import pytest
from business_object.joueurs import Joueur
from business_object.distrib import Distrib


@pytest.fixture
def joueurs():
    """Crée une liste de 3 joueurs avec un solde initial."""
    return [Joueur(pseudo=f"Joueur{i}", solde=1000) for i in range(1, 4)]


@pytest.fixture
def distrib(joueurs):
    """Crée une instance de Distrib avec les joueurs."""
    return Distrib(joueurs=joueurs)


# === Tests d’initialisation ===

def test_initialisation_valide(joueurs):
    d = Distrib(joueurs=joueurs)
    assert len(d.joueurs) == 3
    assert d.deck is not None
    assert d.flop == []
    assert d.turn is None
    assert d.river is None
    assert d.tour_actuel == "preflop"


@pytest.mark.parametrize("nb_joueurs", [1, 6])
def test_initialisation_invalide_nombre_joueurs(nb_joueurs):
    joueurs = [Joueur(pseudo=f"Joueur{i}", solde=1000) for i in range(1, nb_joueurs + 1)]
    with pytest.raises(ValueError, match="Le nombre de joueurs doit être compris entre 2 et 5."):
        Distrib(joueurs=joueurs)


# === Tests sur les joueurs actifs ===

def test_joueurs_actifs_et_partie_terminee(distrib):
    assert len(distrib.joueurs_actifs()) == 3
    assert not distrib.partie_terminee()

    distrib.joueurs[0].se_coucher()
    assert len(distrib.joueurs_actifs()) == 2
    assert not distrib.partie_terminee()

    distrib.joueurs[1].se_coucher()
    assert len(distrib.joueurs_actifs()) == 1
    assert distrib.partie_terminee()


# === Tests de distribution ===

def test_distribuer_mains(distrib):
    distrib.distribuer_mains()
    for joueur in distrib.joueurs:
        assert len(joueur.main) == 2
    total_cartes_tirees = 2 * len(distrib.joueurs)
    assert len(distrib.deck.cartes) == 52 - total_cartes_tirees
    assert distrib.tour_actuel == "preflop"


def test_distribuer_flop(distrib):
    distrib.distribuer_mains()
    distrib.distribuer_flop()
    assert len(distrib.flop) == 3
    assert distrib.tour_actuel == "flop"


def test_distribuer_flop_partie_terminee(distrib, capsys):
    distrib.joueurs[0].se_coucher()
    distrib.joueurs[1].se_coucher()
    distrib.distribuer_flop()
    captured = capsys.readouterr()
    assert "Fin de la main" in captured.out
    assert distrib.flop == []  # aucune carte distribuée


def test_distribuer_turn(distrib):
    distrib.distribuer_mains()
    distrib.distribuer_flop()
    distrib.distribuer_turn()
    assert distrib.turn is not None
    assert distrib.tour_actuel == "turn"


def test_distribuer_turn_partie_terminee(distrib, capsys):
    distrib.joueurs[0].se_coucher()
    distrib.joueurs[1].se_coucher()
    distrib.distribuer_turn()
    captured = capsys.readouterr()
    assert "Fin de la main" in captured.out
    assert distrib.turn is None


def test_distribuer_river(distrib):
    distrib.distribuer_mains()
    distrib.distribuer_flop()
    distrib.distribuer_turn()
    distrib.distribuer_river()
    assert distrib.river is not None
    assert distrib.tour_actuel == "river"


def test_distribuer_river_partie_terminee(distrib, capsys):
    distrib.joueurs[0].se_coucher()
    distrib.joueurs[1].se_coucher()
    distrib.distribuer_river()
    captured = capsys.readouterr()
    assert "Fin de la main" in captured.out
    assert distrib.river is None


# === Test global ===

def test_sequence_complete(distrib):
    distrib.distribuer_mains()
    distrib.distribuer_flop()
    distrib.distribuer_turn()
    distrib.distribuer_river()
    assert len(distrib.flop) == 3
    assert distrib.turn is not None
    assert distrib.river is not None
    assert distrib.tour_actuel == "river"