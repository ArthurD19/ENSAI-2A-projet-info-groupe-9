import pytest
from cartes import Carte, couleurs, valeurs, combinaisons
from evaluateur import EvaluateurMain


def build_ev(cartes):
    return EvaluateurMain(cartes).evalue_main()


def test_hauteur():
    cartes = [
        Carte(couleurs.COEUR, valeurs.DEUX),
        Carte(couleurs.PIQUE, valeurs.TROIS),
        Carte(couleurs.CARREAU, valeurs.QUATRE),
        Carte(couleurs.TREFLE, valeurs.SIX),
        Carte(couleurs.COEUR, valeurs.DAME),
    ]
    assert build_ev(cartes) == combinaisons.HAUTEUR


def test_paire():
    cartes = [
        Carte(couleurs.COEUR, valeurs.DEUX),
        Carte(couleurs.PIQUE, valeurs.DEUX),
        Carte(couleurs.CARREAU, valeurs.QUATRE),
        Carte(couleurs.TREFLE, valeurs.SIX),
        Carte(couleurs.COEUR, valeurs.DAME),
    ]
    assert build_ev(cartes) == combinaisons.PAIRE


def test_double_paire():
    cartes = [
        Carte(couleurs.COEUR, valeurs.DEUX),
        Carte(couleurs.PIQUE, valeurs.DEUX),
        Carte(couleurs.CARREAU, valeurs.QUATRE),
        Carte(couleurs.TREFLE, valeurs.QUATRE),
        Carte(couleurs.COEUR, valeurs.DAME),
    ]
    assert build_ev(cartes) == combinaisons.DOUBLE_PAIRE


def test_brelan():
    cartes = [
        Carte(couleurs.COEUR, valeurs.DEUX),
        Carte(couleurs.PIQUE, valeurs.DEUX),
        Carte(couleurs.CARREAU, valeurs.DEUX),
        Carte(couleurs.TREFLE, valeurs.SIX),
        Carte(couleurs.COEUR, valeurs.DAME),
    ]
    assert build_ev(cartes) == combinaisons.BRELAN


def test_suite():
    cartes = [
        Carte(couleurs.COEUR, valeurs.CINQ),
        Carte(couleurs.PIQUE, valeurs.SIX),
        Carte(couleurs.CARREAU, valeurs.SEPT),
        Carte(couleurs.TREFLE, valeurs.HUIT),
        Carte(couleurs.COEUR, valeurs.NEUF),
    ]
    assert build_ev(cartes) == combinaisons.QUINTE


def test_couleur():
    cartes = [
        Carte(couleurs.COEUR, valeurs.DEUX),
        Carte(couleurs.COEUR, valeurs.QUATRE),
        Carte(couleurs.COEUR, valeurs.SIX),
        Carte(couleurs.COEUR, valeurs.HUIT),
        Carte(couleurs.COEUR, valeurs.DAME),
    ]
    assert build_ev(cartes) == combinaisons.COULEUR


def test_full():
    cartes = [
        Carte(couleurs.COEUR, valeurs.DEUX),
        Carte(couleurs.PIQUE, valeurs.DEUX),
        Carte(couleurs.CARREAU, valeurs.DEUX),
        Carte(couleurs.TREFLE, valeurs.DAME),
        Carte(couleurs.COEUR, valeurs.DAME),
    ]
    assert build_ev(cartes) == combinaisons.FULL


def test_carre():
    cartes = [
        Carte(couleurs.COEUR, valeurs.DEUX),
        Carte(couleurs.PIQUE, valeurs.DEUX),
        Carte(couleurs.CARREAU, valeurs.DEUX),
        Carte(couleurs.TREFLE, valeurs.DEUX),
        Carte(couleurs.COEUR, valeurs.DAME),
    ]
    assert build_ev(cartes) == combinaisons.CARRE


def test_quinte_flush():
    cartes = [
        Carte(couleurs.COEUR, valeurs.CINQ),
        Carte(couleurs.COEUR, valeurs.SIX),
        Carte(couleurs.COEUR, valeurs.SEPT),
        Carte(couleurs.COEUR, valeurs.HUIT),
        Carte(couleurs.COEUR, valeurs.NEUF),
    ]
    assert build_ev(cartes) == combinaisons.QUINTE_FLUSH


def test_quinte_flush_royale():
    cartes = [
        Carte(couleurs.COEUR, valeurs.DIX),
        Carte(couleurs.COEUR, valeurs.VALET),
        Carte(couleurs.COEUR, valeurs.DAME),
        Carte(couleurs.COEUR, valeurs.ROI),
        Carte(couleurs.COEUR, valeurs.AS),
    ]
    assert build_ev(cartes) == combinaisons.QUINTE_FLUSH_ROYALE


def test_comparer_mains():
    main1 = combinaisons.COULEUR
    main2 = combinaisons.PAIRE
    assert EvaluateurMain.comparer_mains(main1, main2) == 1
    assert EvaluateurMain.comparer_mains(main2, main1) == -1
    assert EvaluateurMain.comparer_mains(main1, main1) == 0
