# test_partie_service_pytest.py
import pytest
from business_object.table import Table
from business_object.partie import Partie, EtatPartie
from business_object.joueurs import Joueur
from service.partie_service import PartieService

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


"""
def test_limite_joueurs(partie_service):
    # Créer 5 joueurs pour remplir la table et la liste d'attente
    joueurs = [Joueur(f"j{i}", solde=100) for i in range(5)]
    for j in joueurs:
        partie_service.rejoindre_partie(j)
    # Ajouter un joueur supplémentaire
    joueur_extra = Joueur("extra", solde=100)
    success, etat, msg = partie_service.rejoindre_partie(joueur_extra)
    assert success is False
    assert "pleines" in msg
"""