import pytest
from business_object.cartes import Carte, valeurs, couleurs
from business_object.joueurs import Joueur
from business_object.table import Table
from business_object.partie import Partie
from business_object.comptage import Comptage

@pytest.fixture
def table_exemple():
    t = Table(id=1)
    t.ajouter_joueur(Joueur("Alice", 1000))
    t.ajouter_joueur(Joueur("Bob", 1000))
    return t

def test_init_partie(table_exemple):
    partie = Partie(id=1, table=table_exemple)
    
    assert partie.id == 1
    assert partie.table == table_exemple
    assert partie.distrib is not None
    assert partie.comptage is not None
    assert partie.tour_actuel == "preflop"
    assert partie.mise_max == 0
    assert partie.indice_joueur_courant == 0
    
    assert len(partie.table.joueurs) == 2
    pseudos = [j.pseudo for j in partie.table.joueurs]
    assert "Alice" in pseudos
    assert "Bob" in pseudos

@pytest.fixture
def table_exemple_blinds():
    t = Table(id=1)
    t.ajouter_joueur(Joueur("Alice", 1000))
    t.ajouter_joueur(Joueur("Bob", 1000))
    t.ajouter_joueur(Joueur("Charlie", 1000))
    t.indice_dealer = 0  
    return t

def test_initialiser_blinds(table_exemple_blinds):

    partie = Partie(id=1, table=table_exemple_blinds)
    partie.initialiser_blinds()

    alice = table_exemple_blinds.joueurs[0]  
    bob = table_exemple_blinds.joueurs[1]    
    charlie = table_exemple_blinds.joueurs[2]  
    assert alice.mise == 10
    assert bob.mise == 20
    assert charlie.mise == 0
    assert partie.mise_max == 20
    assert partie.indice_joueur_courant == 2  

@pytest.fixture
def table_etat():
    t = Table(id=1)
    t.ajouter_joueur(Joueur("Alice", 1000))
    t.ajouter_joueur(Joueur("Bob", 1000))
    t.indice_dealer = 0
    return t

def test_afficher_etat(table_etat, capsys):
    partie = Partie(1, table_etat)
    partie.comptage = Comptage()  
    partie.afficher_etat()
    
    captured = capsys.readouterr()
    # Vérifie que les pseudos des joueurs apparaissent
    assert "Alice" in captured.out
    assert "Bob" in captured.out
    # Vérifie que le pot principal est affiché
    assert "Pot principal" in captured.out

def test_passer_tour(table_etat):
    partie = Partie(1, table_etat)
    alice, bob = table_etat.joueurs

    alice.miser(50)
    bob.miser(30)
    partie.mise_max = 50

    partie.passer_tour()

    assert partie.comptage.pot == 80
    assert alice.mise == 0
    assert bob.mise == 0
    assert partie.mise_max == 0

def test_affrontement_mains(monkeypatch):
    # Création de la table avec 2 joueurs
    table = Table(id=1)
    alice = Joueur("Alice", 1000)
    bob = Joueur("Bob", 1000)
    table.ajouter_joueur(alice)
    table.ajouter_joueur(bob)
    partie = Partie(1, table)

    # Board fixe
    board = [
        Carte(couleurs.COEUR, valeurs.AS),
        Carte(couleurs.COEUR, valeurs.ROI),
        Carte(couleurs.COEUR, valeurs.DAME),
        Carte(couleurs.PIQUE, valeurs.TROIS),
        Carte(couleurs.CARREAU, valeurs.DEUX)
    ]
    partie.table.board = board

    # Mains des joueurs
    alice.main = [
        Carte(couleurs.COEUR, valeurs.DIX),
        Carte(couleurs.COEUR, valeurs.VALET)
    ]  # Quinte flush
    bob.main = [
        Carte(couleurs.PIQUE, valeurs.AS),
        Carte(couleurs.TREFLE, valeurs.AS)
    ]  # Paire d'As

    # Pot de test
    partie.comptage.pot = 100

    # Monkeypatch pour bypass input()
    monkeypatch.setattr("builtins.input", lambda x: "suivre")

    # Lancer l'annonce des résultats
    partie.annoncer_resultats()

    # Vérifie que Alice remporte le pot
    assert alice.solde > 1000
    assert bob.solde == 1000