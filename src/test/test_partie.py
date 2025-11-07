import pytest
from business_object.partie import Partie
from business_object.joueurs import Joueur
from business_object.table import Table
from business_object.cartes import Carte, couleurs, valeurs


@pytest.fixture
def setup_partie():
    # Crée 2 joueurs
    j1 = Joueur("Alice", solde=100)
    j2 = Joueur("Bob", solde=100)
    
    # Crée la table
    table = Table(id=1)
    table.ajouter_joueur(j1)
    table.ajouter_joueur(j2)
    
    # Crée la partie
    partie = Partie(id=1, table=table)
    
    return partie, j1, j2


def test_initialiser_blinds(setup_partie):
    partie, j1, j2 = setup_partie
    partie.initialiser_blinds()
    
    # Vérifie que les blinds ont été mises
    assert any(j["pseudo"] == "Alice" and j["mise"] > 0 for j in partie.etat.joueurs)
    assert any(j["pseudo"] == "Bob" and j["mise"] > 0 for j in partie.etat.joueurs)


def test_actions_joueur_miser(setup_partie):
    partie, j1, j2 = setup_partie
    partie.initialiser_blinds()
    
    # Alice mise 30 (total = 30 + sa blind)
    etat = partie.actions_joueur("Alice", "miser", 30)
    alice = next(j for j in etat.joueurs if j["pseudo"] == "Alice")
    assert alice["mise"] == 30 + 20  


def test_actions_joueur_suivre(setup_partie):
    partie, j1, j2 = setup_partie
    partie.initialiser_blinds()
    
    # Alice mise 30, Bob suit
    partie.actions_joueur("Alice", "miser", 30)
    etat = partie.actions_joueur("Bob", "suivre")
    bob = next(j for j in etat.joueurs if j["pseudo"] == "Bob")
    assert bob["mise"] == partie.mise_max  # Bob a suivi la mise max


def test_actions_joueur_se_coucher(setup_partie):
    partie, j1, j2 = setup_partie
    partie.initialiser_blinds()
    
    etat = partie.actions_joueur("Alice", "se_coucher")
    alice = next(j for j in etat.joueurs if j["pseudo"] == "Alice")
    assert alice["actif"] is False


def test_actions_joueur_all_in(setup_partie):
    partie, j1, j2 = setup_partie
    partie.initialiser_blinds()

    etat_avant = next(j for j in partie.etat.joueurs if j["pseudo"] == "Alice")
    solde_alice = etat_avant["solde"]

    etat = partie.actions_joueur("Alice", "all-in")
    alice = next(j for j in etat.joueurs if j["pseudo"] == "Alice")
    assert alice["mise"] == solde_alice + 20  
    assert alice["actif"] is True


def test_passer_tour(setup_partie):
    partie, j1, j2 = setup_partie
    partie.initialiser_blinds()
    
    partie.actions_joueur("Alice", "miser", 30)
    partie.actions_joueur("Bob", "suivre")
    
    partie.passer_tour()
    etat = partie.etat
    total_pot_attendu = sum(j.mise for j in partie.table.joueurs) + partie.comptage.pot
    assert etat.pot == total_pot_attendu


def test_annoncer_resultats(setup_partie):
    partie, j1, j2 = setup_partie
    partie.initialiser_blinds()

    # Distribuer mains et board pour avoir 5 cartes au total
    j1.main = [Carte(couleurs.COEUR, valeurs.AS), Carte(couleurs.COEUR, valeurs.ROI)]
    j2.main = [Carte(couleurs.PIQUE, valeurs.DAME), Carte(couleurs.PIQUE, valeurs.VALET)]
    partie.table.board = [
        Carte(couleurs.COEUR, valeurs.DIX),
        Carte(couleurs.CARREAU, valeurs.NEUF),
        Carte(couleurs.TREFLE, valeurs.HUIT)
    ]

    partie.actions_joueur("Alice", "miser", 20)
    partie.actions_joueur("Bob", "suivre")

    assert partie.etat.pot > 0