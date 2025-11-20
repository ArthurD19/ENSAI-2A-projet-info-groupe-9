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


def test_miser_mise_interdite_si_inferieure_au_minimum(monkeypatch):
    # Fake DAO qui dit que le joueur existe et a de l'argent
    class FakeJoueurDao:
        def valeur_portefeuille(self, pseudo):
            return 200

        def existe_joueur(self, pseudo):
            return True

    monkeypatch.setattr(
        "src.dao.joueur_dao.JoueurDao",
        FakeJoueurDao
    )

    # --- Préparation de la partie ---
    table = Table(id=1, blind=20)
    partie = Partie(id=1, table=table)

    partie.GROSSE_BLIND = 20

    service = PartieService(partie)

    # --- Ajouter un joueur ---
    joueur = Joueur("lucas", solde=200)
    table.ajouter_joueur(joueur)
    joueur.mise = 0

    # Mise trop faible : 10 < 40 et != 20
    success, etat, msg = service.miser("lucas", 30)

    # --- Vérifications ---
    assert success is False
    assert "grosse blinde" in msg.lower(), f"Message incorrect : {msg}"


def test_miser_limite_max(monkeypatch):
    # --- Setup partie et service ---
    table = Table(id=1, blind=20)
    partie = Partie(id=1, table=table)
    service = PartieService(partie)

    # Ajouter joueurs
    joueur_pauvre = Joueur("pauvre", solde=50)
    joueur_riche = Joueur("riche", solde=200)
    table.ajouter_joueur(joueur_pauvre)
    table.ajouter_joueur(joueur_riche)

    # --- Test mise dépassant la limite ---
    success, etat, msg = service.miser("riche", 60)
    assert success is False, "La mise dépasse la limite max, devrait échouer"
    assert "tu ne peux pas miser plus que" in msg.lower()
    assert "50" in msg

    # --- Test mise égale à la limite (doit réussir) ---
    success, etat, msg = service.miser("riche", 50)
    assert success is True, "La mise égale à la limite max devrait réussir"
    assert msg == ""


def test_all_in_limite_max(monkeypatch):
    # --- Setup partie et service ---
    table = Table(id=1, blind=20)
    partie = Partie(id=1, table=table)
    service = PartieService(partie)

    # Ajouter joueurs
    joueur_pauvre = Joueur("pauvre", solde=50)
    joueur_riche = Joueur("riche", solde=200)
    table.ajouter_joueur(joueur_pauvre)
    table.ajouter_joueur(joueur_riche)

    # --- Test all-in du joueur riche (doit échouer) ---
    success, etat, msg = service.all_in("riche")
    assert success is False, "All-in dépasse la limite max, devrait échouer"
    assert "tu ne peux pas all-in" in msg.lower()
    assert "50" in msg

    # --- Test all-in du joueur pauvre (doit réussir) ---
    success, etat, msg = service.all_in("pauvre")
    assert success is True, "All-in inférieur à la limite max devrait réussir"
    assert msg == ""

# ---------------------------
# TEST voir_etat_partie
# ---------------------------


def test_voir_etat_partie_retourne_etat(partie_service, joueur_lucas):
    partie_service.partie.table.ajouter_joueur(joueur_lucas)
    success, etat, msg = partie_service.voir_etat_partie()
    assert success is True
    assert isinstance(etat, EtatPartie)
    assert msg == ""

# ---------------------------
# TEST suivre
# ---------------------------


def test_suivre_partie(partie_service):
    joueur = Joueur("lucas", solde=100)
    partie_service.partie.table.ajouter_joueur(joueur)
    partie_service.partie.mise_max = 20
    joueur.mise = 0

    success, etat, msg = partie_service.suivre("lucas")
    assert success is True
    assert msg == ""



def test_suivre_solde_insuffisant(partie_service):
    joueur = Joueur("lucas", solde=10)
    partie_service.partie.table.ajouter_joueur(joueur)
    partie_service.partie.mise_max = 20
    joueur.mise = 0

    success, etat, msg = partie_service.suivre("lucas")
    assert success is False
    assert "dépasse ton solde" in msg.lower()

# ---------------------------
# TEST decision_rejouer
# ---------------------------


def test_decision_rejouer_oui(partie_service):
    partie_service.partie.etat.rejouer = {"lucas": None}

    success, etat, msg = partie_service.decision_rejouer("lucas", True)
    assert success is True
    assert "veut rejouer" in msg.lower()


def test_decision_rejouer_non(partie_service):
    partie_service.partie.etat.rejouer = {"lucas": None}

    success, etat, msg = partie_service.decision_rejouer("lucas", False)
    assert success is True
    assert "quitte la table" in msg.lower()


def test_decision_rejouer_joueur_pas_present(partie_service):
    joueur = "lucas"
    success, etat, msg = partie_service.decision_rejouer(joueur, True)
    assert success is False
    assert "n'était pas dans la main précédente" in msg.lower()
