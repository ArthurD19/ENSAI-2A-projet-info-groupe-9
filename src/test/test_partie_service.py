# test_partie_service_pytest.py
import pytest
from src.business_object.table import Table
from src.business_object.partie import Partie, EtatPartie
from src.business_object.joueurs import Joueur
from src.service.partie_service import PartieService
from src.service.table_service import TableService

@pytest.fixture
def table_exemple():
    t = Table(id=1, blind=20)
    return t

@pytest.fixture
def partie_service(table_exemple):
    partie = Partie(id=1, table=table_exemple)
    service = PartieService(partie)
    return service

@pytest.fixture
def joueur_lucas():
    return Joueur(pseudo="lucas", solde=100)

@pytest.fixture
def joueur_marie():
    return Joueur(pseudo="marie", solde=50)

def test_rejoindre_partie_ok(partie_service, joueur_lucas):
    # Ajouter le joueur à la table comme le ferait rejoindre_table
    partie_service.partie.table.ajouter_joueur(joueur_lucas)
    
    success, etat, msg = partie_service.rejoindre_partie(joueur_lucas)
    assert success is True


def test_rejoindre_partie_solde_insuffisant(partie_service):
    joueur_pauvre = Joueur(pseudo="pauvre", solde=5)
    success, etat, msg = partie_service.rejoindre_partie(joueur_pauvre)
    assert success is False
    assert "pas assez de jetons" in msg

def test_rejoindre_partie_liste_attente(partie_service):
    # Simuler une partie en cours
    partie_service.partie.etat.finie = False

    # Ajouter 2 joueurs dans la table (déjà en cours)
    joueur1 = Joueur("Alice", 100)
    joueur2 = Joueur("Bob", 100)
    partie_service.partie.table.ajouter_joueur(joueur1)
    partie_service.partie.table.ajouter_joueur(joueur2)

    # Joueur qui arrive pendant la partie en cours
    joueur3 = Joueur("Charlie", 100)
    success, etat, msg = partie_service.rejoindre_partie(joueur3)

    # Vérifier que la réponse est correcte
    assert success is True
    assert "liste d'attente" in msg
    assert any(j["pseudo"] == "Charlie" for j in etat.liste_attente)

    # Vérifier qu'on ne l'a pas ajouté directement à la table
    assert all(j.pseudo != "Charlie" for j in partie_service.partie.table.joueurs)

class FakeJoueurDao:
    def valeur_portefeuille(self, pseudo):
        return 100

@pytest.fixture(autouse=True)
def patch_joueur_dao(monkeypatch):
    monkeypatch.setattr("src.dao.joueur_dao.JoueurDao", FakeJoueurDao)
    return FakeJoueurDao()

@pytest.fixture
def service():
    return TableService(nb_tables=1, blind=20)

def test_rejoindre_table_ajoute_bien_le_joueur_dans_la_table(service):
    """Test 1 : vérifier uniquement que le joueur est dans la table."""
    pseudo = "lucas"

    success, etat, msg = service.rejoindre_table(pseudo, 1)

    table = service.get_table(1)

    assert success is True
    assert any(j.pseudo == pseudo for j in table.joueurs)

def test_rejoindre_table_ajoute_joueur_a_la_partie(service):
    """Test 2 : le joueur doit apparaître soit dans les joueurs de la partie,
    soit dans la liste d’attente selon l’état de la partie."""
    
    pseudo = "lucas"

    success, etat, msg = service.rejoindre_table(pseudo, 1)
    partie = service.parties[1]

    # Vérifie si le joueur est dans la table active
    est_dans_partie = any(j.pseudo == pseudo for j in partie.table.joueurs)

    # Vérifie si le joueur est en liste d’attente
    est_en_attente = any(
        (j["pseudo"] if isinstance(j, dict) else j.pseudo) == pseudo 
        for j in partie.etat.liste_attente
    )

    assert est_dans_partie or est_en_attente, \
        f"{pseudo} n'est ni dans la partie ni dans la liste d'attente."

def test_rejoindre_table_interdit_deux_fois(service):
    """On ne doit pas pouvoir rejoindre deux fois la même table avec le même joueur."""
    
    pseudo = "enzo"

    # Premier appel : OK
    success1, etat1, msg1 = service.rejoindre_table(pseudo, 1)
    assert success1 is True

    # Deuxième appel : doit être refusé
    success2, etat2, msg2 = service.rejoindre_table(pseudo, 1)

    assert success2 is False, "Le même joueur ne doit pas pouvoir rejoindre la table deux fois."
    assert "déjà" in msg2.lower() or "existe" in msg2.lower(), \
    f"Le message devrait indiquer que le joueur est déjà présent. Reçu : {msg2}"