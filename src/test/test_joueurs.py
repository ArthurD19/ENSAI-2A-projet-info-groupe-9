import pytest
from src.business_object.cartes import Carte, Deck, couleurs, valeurs
from src.business_object.joueurs import Joueur


def test_initialisation_joueur():
    j = Joueur("Alice", 1000)
    assert j.pseudo == "Alice"
    assert j.solde == 1000
    assert j.main == []
    assert j.mise == 0
    assert j.actif


def test_recevoir_carte():
    j = Joueur("Bob", 1000)
    c1 = Carte(couleurs.COEUR, valeurs.DEUX)
    c2 = Carte(couleurs.PIQUE, valeurs.AS)
    j.recevoir_carte(c1)
    j.recevoir_carte(c2)
    assert j.main == [c1, c2]

    c3 = Carte(couleurs.CARREAU, valeurs.TROIS)
    with pytest.raises(ValueError):
        j.recevoir_carte(c3)


def test_recevoir_du_deck():
    deck = Deck()
    deck.remplir()
    j = Joueur("Charlie", 50)
    j.recevoir_du_deck(deck)
    j.recevoir_du_deck(deck)
    assert len(j.main) == 2
    assert len(deck.cartes) == 50


def test_reset_main():
    j = Joueur("Alice", 100)
    j.main = [Carte(couleurs.COEUR, valeurs.CINQ)]
    j.mise = 20
    j.actif = False
    j.reset_main()
    assert j.main == []
    assert j.mise == 0
    assert j.actif


def test_miser_et_suivre():
    j = Joueur("Bob", 100)
    montant = j.miser(30)
    assert montant == 30
    assert j.mise == 30
    assert j.solde == 70

    j2 = Joueur("Charlie", 50)
    j2.miser(10)
    j2.suivre(30)
    assert j2.mise == 30
    assert j2.solde == 20

    with pytest.raises(ValueError):
        j2.miser(100)


def test_se_coucher():
    j = Joueur("Alice", 50)
    j.se_coucher()
    assert not j.actif


def test_repr():
    j = Joueur("Bob", 75)
    c = Carte(couleurs.COEUR, valeurs.ROI)
    j.recevoir_carte(c)
    r = repr(j)
    assert "Bob" in r
    assert repr(c) in r
