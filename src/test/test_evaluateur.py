import pytest
from src.business_object.cartes import Carte, valeurs, couleurs, combinaisons
from src.business_object.evaluateur import EvaluateurMain

def carte(valeur, couleur):
    """Créer une carte."""
    return Carte(valeur=valeur, couleur=couleur)


def test_quinte_flush_royaale():
    cartes = [
        carte(valeurs.DIX, couleurs.COEUR),
        carte(valeurs.VALET, couleurs.COEUR),
        carte(valeurs.DAME, couleurs.COEUR),
        carte(valeurs.ROI, couleurs.COEUR),
        carte(valeurs.AS, couleurs.COEUR),
        carte(valeurs.DEUX, couleurs.PIQUE),
        carte(valeurs.TROIS, couleurs.CARREAU)
    ]
    evaluateur = EvaluateurMain(cartes)
    assert evaluateur.evalue_main().combinaison == combinaisons.QUINTE_FLUSH_ROYALE


def test_carre():
    cartes = [
        carte(valeurs.AS, couleurs.COEUR),
        carte(valeurs.AS, couleurs.PIQUE),
        carte(valeurs.AS, couleurs.CARREAU),
        carte(valeurs.AS, couleurs.TREFLE),
        carte(valeurs.DAME, couleurs.COEUR),
        carte(valeurs.TROIS, couleurs.PIQUE),
        carte(valeurs.CINQ, couleurs.CARREAU)
    ]
    evaluateur = EvaluateurMain(cartes)
    assert evaluateur.evalue_main().combinaison == combinaisons.CARRE


def test_full():
    cartes = [
        carte(valeurs.DAME, couleurs.COEUR),
        carte(valeurs.DAME, couleurs.PIQUE),
        carte(valeurs.DAME, couleurs.CARREAU),
        carte(valeurs.ROI, couleurs.TREFLE),
        carte(valeurs.ROI, couleurs.COEUR),
        carte(valeurs.DEUX, couleurs.PIQUE),
        carte(valeurs.TROIS, couleurs.CARREAU)
    ]
    evaluateur = EvaluateurMain(cartes)
    assert evaluateur.evalue_main().combinaison == combinaisons.FULL


def test_flush():
    cartes = [
        carte(valeurs.DEUX, couleurs.COEUR),
        carte(valeurs.CINQ, couleurs.COEUR),
        carte(valeurs.SEPT, couleurs.COEUR),
        carte(valeurs.NEUF, couleurs.COEUR),
        carte(valeurs.ROI, couleurs.COEUR),
        carte(valeurs.TROIS, couleurs.PIQUE)
    ]
    evaluateur = EvaluateurMain(cartes)
    assert evaluateur.evalue_main().combinaison == combinaisons.COULEUR


def test_straight():
    cartes = [
        carte(valeurs.CINQ, couleurs.COEUR),
        carte(valeurs.SIX, couleurs.PIQUE),
        carte(valeurs.SEPT, couleurs.CARREAU),
        carte(valeurs.HUIT, couleurs.TREFLE),
        carte(valeurs.NEUF, couleurs.COEUR),
        carte(valeurs.DEUX, couleurs.PIQUE)
    ]
    evaluateur = EvaluateurMain(cartes)
    assert evaluateur.evalue_main().combinaison == combinaisons.QUINTE


def test_brelan():
    cartes = [
        carte(valeurs.TROIS, couleurs.COEUR),
        carte(valeurs.TROIS, couleurs.PIQUE),
        carte(valeurs.TROIS, couleurs.CARREAU),
        carte(valeurs.CINQ, couleurs.TREFLE),
        carte(valeurs.SEPT, couleurs.COEUR)
    ]
    evaluateur = EvaluateurMain(cartes)
    assert evaluateur.evalue_main().combinaison == combinaisons.BRELAN


def test_double_paire():
    cartes = [
        carte(valeurs.SEPT, couleurs.COEUR),
        carte(valeurs.SEPT, couleurs.PIQUE),
        carte(valeurs.CINQ, couleurs.CARREAU),
        carte(valeurs.CINQ, couleurs.TREFLE),
        carte(valeurs.AS, couleurs.COEUR)
    ]
    evaluateur = EvaluateurMain(cartes)
    result = evaluateur.evalue_main()
    assert result.combinaison == combinaisons.DOUBLE_PAIRE
    assert result.tiebreaker_cards[:2] == [valeurs.SEPT, valeurs.CINQ]
    assert result.tiebreaker_cards[2] == valeurs.AS


def test_paire():
    cartes = [
        carte(valeurs.AS, couleurs.COEUR),
        carte(valeurs.AS, couleurs.PIQUE),
        carte(valeurs.TROIS, couleurs.CARREAU),
        carte(valeurs.CINQ, couleurs.TREFLE),
        carte(valeurs.SEPT, couleurs.COEUR)
    ]
    evaluateur = EvaluateurMain(cartes)
    result = evaluateur.evalue_main()
    assert result.combinaison == combinaisons.PAIRE
    assert result.tiebreaker_cards[0] == valeurs.AS


def test_hauteur():
    cartes = [
        carte(valeurs.DEUX, couleurs.COEUR),
        carte(valeurs.CINQ, couleurs.PIQUE),
        carte(valeurs.SEPT, couleurs.CARREAU),
        carte(valeurs.NEUF, couleurs.TREFLE),
        carte(valeurs.ROI, couleurs.COEUR)
    ]
    evaluateur = EvaluateurMain(cartes)
    result = evaluateur.evalue_main()
    assert result.combinaison == combinaisons.HAUTEUR
    assert result.tiebreaker_cards[0] == valeurs.ROI


def test_comparer_diff_combinaisons():
    cartes1 = [
        carte(valeurs.SEPT, couleurs.COEUR),
        carte(valeurs.SEPT, couleurs.PIQUE),
        carte(valeurs.CINQ, couleurs.CARREAU),
        carte(valeurs.CINQ, couleurs.TREFLE),
        carte(valeurs.AS, couleurs.COEUR)
    ]  # Double paire
    cartes2 = [
        carte(valeurs.AS, couleurs.COEUR),
        carte(valeurs.AS, couleurs.PIQUE),
        carte(valeurs.TROIS, couleurs.CARREAU),
        carte(valeurs.CINQ, couleurs.TREFLE),
        carte(valeurs.SEPT, couleurs.COEUR)
    ]  # Paire
    eval1 = EvaluateurMain(cartes1).evalue_main()
    eval2 = EvaluateurMain(cartes2).evalue_main()
    assert EvaluateurMain.comparer_mains(eval1, eval2) == 1
    assert EvaluateurMain.comparer_mains(eval2, eval1) == -1


def test_comparer_egalite():
    cartes1 = [
        carte(valeurs.SEPT, couleurs.COEUR),
        carte(valeurs.SEPT, couleurs.PIQUE),
        carte(valeurs.CINQ, couleurs.CARREAU),
        carte(valeurs.CINQ, couleurs.TREFLE),
        carte(valeurs.AS, couleurs.COEUR)
    ]
    cartes2 = [
        carte(valeurs.SEPT, couleurs.TREFLE),
        carte(valeurs.SEPT, couleurs.CARREAU),
        carte(valeurs.CINQ, couleurs.COEUR),
        carte(valeurs.CINQ, couleurs.PIQUE),
        carte(valeurs.AS, couleurs.PIQUE)
    ]
    eval1 = EvaluateurMain(cartes1).evalue_main()
    eval2 = EvaluateurMain(cartes2).evalue_main()
    assert EvaluateurMain.comparer_mains(eval1, eval2) == 0

def test_valeurs_numeriques_et_compter_occurrences():
    cartes = [
        carte(valeurs.AS, couleurs.COEUR),
        carte(valeurs.DEUX, couleurs.PIQUE),
        carte(valeurs.TROIS, couleurs.CARREAU),
        carte(valeurs.DEUX, couleurs.TREFLE),
        carte(valeurs.AS, couleurs.PIQUE)
    ]
    evaluateur = EvaluateurMain(cartes)
    valeurs_num = evaluateur._valeurs_numeriques()
    counts = evaluateur._compter_occurrences()
    # valeurs triées desc
    assert valeurs_num == [14, 14, 3, 2, 2]
    # compteur correct
    assert counts[14] == 2
    assert counts[2] == 2
    assert counts[3] == 1

def test_is_flush_true_et_false():
    cartes_flush = [
        carte(valeurs.AS, couleurs.COEUR),
        carte(valeurs.DEUX, couleurs.COEUR),
        carte(valeurs.TROIS, couleurs.COEUR),
        carte(valeurs.QUATRE, couleurs.COEUR),
        carte(valeurs.CINQ, couleurs.COEUR)
    ]
    cartes_non_flush = [
        carte(valeurs.AS, couleurs.COEUR),
        carte(valeurs.DEUX, couleurs.PIQUE),
        carte(valeurs.TROIS, couleurs.CARREAU),
        carte(valeurs.QUATRE, couleurs.TREFLE),
        carte(valeurs.CINQ, couleurs.COEUR)
    ]
    evaluateur_flush = EvaluateurMain(cartes_flush)
    evaluateur_non_flush = EvaluateurMain(cartes_non_flush)
    assert evaluateur_flush._is_flush()[0] is True
    assert evaluateur_non_flush._is_flush()[0] is False

def test_is_straight_true_et_false():
    cartes_straight = [
        carte(valeurs.DEUX, couleurs.COEUR),
        carte(valeurs.TROIS, couleurs.COEUR),
        carte(valeurs.QUATRE, couleurs.PIQUE),
        carte(valeurs.CINQ, couleurs.TREFLE),
        carte(valeurs.SIX, couleurs.COEUR)
    ]
    cartes_non_straight = [
        carte(valeurs.DEUX, couleurs.COEUR),
        carte(valeurs.TROIS, couleurs.PIQUE),
        carte(valeurs.CINQ, couleurs.CARREAU),
        carte(valeurs.SIX, couleurs.TREFLE),
        carte(valeurs.HUIT, couleurs.COEUR)
    ]
    evaluateur_straight = EvaluateurMain(cartes_straight)
    evaluateur_non_straight = EvaluateurMain(cartes_non_straight)
    assert evaluateur_straight._is_straight([2,3,4,5,6])[0] is True
    assert evaluateur_non_straight._is_straight([2,3,5,6,8])[0] is False

def test_numerique_to_enum():
    cartes = [
        carte(valeurs.DEUX, couleurs.COEUR),
        carte(valeurs.TROIS, couleurs.PIQUE),
        carte(valeurs.QUATRE, couleurs.CARREAU),
        carte(valeurs.CINQ, couleurs.TREFLE),
        carte(valeurs.SIX, couleurs.COEUR)
    ]
    evaluateur = EvaluateurMain(cartes)
    # test conversion
    assert evaluateur._numerique_to_enum(2) == valeurs.DEUX
    assert evaluateur._numerique_to_enum(6) == valeurs.SIX
    # valeur non existante renvoie None
    assert evaluateur._numerique_to_enum(100) is None


def test_main_trop_courte_et_longue():
    # moins de 5 cartes
    with pytest.raises(ValueError):
        EvaluateurMain([Carte(valeur=valeurs.AS, couleur='COEUR')] * 4)
    # plus de 7 cartes
    with pytest.raises(ValueError):
        EvaluateurMain([Carte(valeur=valeurs.AS, couleur='COEUR')] * 8)


def test_quinte_flush_simple():
    cartes = [
        Carte(valeur=valeurs.NEUF, couleur='COEUR'),
        Carte(valeur=valeurs.DIX, couleur='COEUR'),
        Carte(valeur=valeurs.VALET, couleur='COEUR'),
        Carte(valeur=valeurs.DAME, couleur='COEUR'),
        Carte(valeur=valeurs.ROI, couleur='COEUR')
    ]
    evaluateur = EvaluateurMain(cartes)
    resultat = evaluateur.evalue_main()
    assert resultat.combinaison == combinaisons.QUINTE_FLUSH
    # les valeurs triées doivent être de la quinte
    assert [v for v in resultat.tiebreaker_cards] == [valeurs.ROI, valeurs.DAME, valeurs.VALET, valeurs.DIX, valeurs.NEUF]

def test_comparer_mains_retour_159_161():
    # main1: paire d'As
    cartes1 = [
        Carte(valeur=valeurs.AS, couleur='COEUR'),
        Carte(valeur=valeurs.AS, couleur='PIQUE'),
        Carte(valeur=valeurs.TROIS, couleur='CARREAU'),
        Carte(valeur=valeurs.CINQ, couleur='TREFLE'),
        Carte(valeur=valeurs.SEPT, couleur='COEUR')
    ]
    # main2: paire de Rois
    cartes2 = [
        Carte(valeur=valeurs.ROI, couleur='COEUR'),
        Carte(valeur=valeurs.ROI, couleur='PIQUE'),
        Carte(valeur=valeurs.DEUX, couleur='CARREAU'),
        Carte(valeur=valeurs.QUATRE, couleur='TREFLE'),
        Carte(valeur=valeurs.SIX, couleur='COEUR')
    ]
    main1 = EvaluateurMain(cartes1).evalue_main()
    main2 = EvaluateurMain(cartes2).evalue_main()
    
    # main1 > main2 → return 1 (ligne 159)
    assert EvaluateurMain.comparer_mains(main1, main2) == 1
    # main2 < main1 → return -1 (ligne 161)
    assert EvaluateurMain.comparer_mains(main2, main1) == -1

def test_quinte_basse_as():
    cartes = [
        Carte(valeur=valeurs.AS, couleur='COEUR'),
        Carte(valeur=valeurs.DEUX, couleur='PIQUE'),
        Carte(valeur=valeurs.TROIS, couleur='CARREAU'),
        Carte(valeur=valeurs.QUATRE, couleur='TREFLE'),
        Carte(valeur=valeurs.CINQ, couleur='COEUR')
    ]
    evaluateur = EvaluateurMain(cartes)
    is_straight, straight_vals = evaluateur._is_straight(evaluateur._valeurs_numeriques())
    assert is_straight is True

    # convertir les valeurs numériques en enums pour comparer
    straight_enums = set(evaluateur._numerique_to_enum(v) for v in straight_vals)
    assert straight_enums == {valeurs.AS, valeurs.DEUX, valeurs.TROIS, valeurs.QUATRE, valeurs.CINQ}
