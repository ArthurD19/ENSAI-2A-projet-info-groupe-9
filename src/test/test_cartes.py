import pytest
from business_object.cartes import Carte, Deck, couleurs, valeurs


def test_Carte_str_repr():
    carte1 = Carte(couleurs.COEUR, valeurs.HUIT)
    carte2 = Carte(couleurs.COEUR, valeurs.TROIS)
    carte3 = Carte(couleurs.PIQUE, valeurs.DEUX)
    assert str(carte1) == "8 de Coeur"
    assert repr(carte1) == "Carte(8, Coeur)"
    assert str(carte2) == "3 de Coeur"
    assert repr(carte2) == "Carte(3, Coeur)"
    assert str(carte3) == "2 de Pique"
    assert repr(carte3) == "Carte(2, Pique)"


def test_Deck_remplir():
    deck = Deck()
    deck.remplir()
    assert len(deck.cartes) == 52
    deck_unique = set(deck.cartes)
    assert len(deck_unique) == 52
    cols = set(c.couleur for c in deck.cartes)
    vals = set(c.valeur for c in deck.cartes)
    assert cols == set(couleurs)   # compare avec Enum
    assert vals == set(valeurs)    # compare avec Enum


def test_deck_melanger():
    deck = Deck()
    deck.remplir()

    avant = deck.cartes.copy()
    deck.melanger()
    apres = deck.cartes
    assert apres != avant

    apres_ord = sorted(str(c) for c in apres)
    avant_ord = sorted(str(c) for c in avant)
    assert apres_ord == avant_ord


def test_deck_tirer():
    deck = Deck()
    with pytest.raises(ValueError):
        deck.tirer()
    deck.remplir()
    carte = deck.tirer()
    assert isinstance(carte, Carte)
    assert len(deck.cartes) == 51


def test_deck_tirer_vide():
    deck = Deck()
    with pytest.raises(ValueError):
        deck.tirer()


def test_deck_len():
    deck = Deck()
    assert len(deck) == 0

    deck.remplir()
    assert len(deck) == 52

    deck.tirer()
    assert len(deck) == 51


def test_deck_ajouter():
    deck = Deck()
    assert len(deck) == 0
    carte = Carte(couleurs.PIQUE, valeurs.AS)
    deck.ajouter(carte)
    assert len(deck) == 1
    assert deck.cartes[0] == carte
