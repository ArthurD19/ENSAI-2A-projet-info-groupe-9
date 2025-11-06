import pytest
from business_object.joueurs import Joueur
from business_object.table import Table
from business_object.comptage import Comptage

@pytest.fixture
def table_exemple():
    t = Table(id=1)
    t.ajouter_joueur(Joueur("Alice", 1000))
    t.ajouter_joueur(Joueur("Bob", 1000))
    return t

@pytest.fixture
def comptage():
    return Comptage()

def test_initialisation_comptage(comptage):
    assert comptage.pot == 0
    assert comptage.pots_perso == {}

def test_ajouter_pot_perso(comptage, table_exemple):
    alice = table_exemple.joueurs[0]
    comptage.ajouter_pot_perso(alice, 100)
    assert comptage.pots_perso == {alice: 100}

def test_ajouter_pot(comptage, table_exemple):
    alice = table_exemple.joueurs[0]
    table_exemple.pot = 200
    comptage.ajouter_pot_perso(alice, table_exemple.pot)
    comptage.ajouter_pot()
    assert comptage.pot == 200

def test_distrib_pots(comptage, table_exemple):
    alice, bob = table_exemple.joueurs
    comptage.ajouter_pot_perso(alice, 100)
    comptage.ajouter_pot_perso(bob, 200)
    comptage.ajouter_pot()
    comptage.distrib_pots([alice, bob])
    assert alice.solde > 1000
    assert bob.solde > 1000
    assert comptage.pot == 0
    assert comptage.pots_perso == {}

def test_distrib_pots_vide(comptage):
    # Aucun gagnant
    comptage.pot = 100
    comptage.pots_perso = {}
    comptage.distrib_pots([])
    # Le pot et les pots perso doivent rester corrects (ou reset)
    assert comptage.pot == 100
    assert comptage.pots_perso == {}

def test_distrib_pots_un_gagnant(comptage, table_exemple):
    alice = table_exemple.joueurs[0]
    comptage.ajouter_pot_perso(alice, 150)
    comptage.ajouter_pot()
    comptage.distrib_pots([alice])
    assert alice.solde == 1150  # 1000 + 150
    assert comptage.pot == 0
    assert comptage.pots_perso == {}

def test_distrib_pots_plusieurs_gagnants(comptage, table_exemple):
    alice, bob = table_exemple.joueurs
    comptage.ajouter_pot_perso(alice, 100)
    comptage.ajouter_pot_perso(bob, 200)
    comptage.ajouter_pot()
    comptage.distrib_pots([alice, bob])
    # Chacun reçoit la moitié du pot total (100 + 200 = 300, donc 150 chacun)
    assert alice.solde == 1150
    assert bob.solde == 1150
    assert comptage.pot == 0
    assert comptage.pots_perso == {}
