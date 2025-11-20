import pytest
from src.business_object.joueurs import Joueur
from src.business_object.distrib import Distrib


@pytest.fixture
def joueurs():
    """Crée une liste de 3 joueurs avec un solde initial."""
    return [Joueur(pseudo=f"Joueur{i}", solde=1000) for i in range(1, 4)]


@pytest.fixture
def distrib(joueurs):
    """Crée une instance de Distrib avec les joueurs."""
    return Distrib(joueurs=joueurs)


def test_initialisation_valide(joueurs):
    d = Distrib(joueurs=joueurs)
    assert len(d.joueurs) == 3
    assert d.deck is not None
    assert d.flop == []
    assert d.turn is None
    assert d.river is None
    assert d.tour_actuel == "preflop"


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


def test_distribuer_turn(distrib):
    distrib.distribuer_mains()
    distrib.distribuer_flop()
    distrib.distribuer_turn()
    assert distrib.turn is not None
    assert distrib.tour_actuel == "turn"


def test_distribuer_river(distrib):
    distrib.distribuer_mains()
    distrib.distribuer_flop()
    distrib.distribuer_turn()
    distrib.distribuer_river()
    assert distrib.river is not None
    assert distrib.tour_actuel == "river"


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


def test_distribuer_flop_un_joueur():
    joueur = Joueur("Solo", 1000)
    d = Distrib([joueur])
    d.distribuer_mains()
    d.distribuer_flop()
    # Comme un seul joueur, le flop ne doit pas être distribué
    assert d.flop == []
    assert d.tour_actuel == "preflop"


def test_distribuer_turn_un_joueur():
    joueur = Joueur("Solo", 1000)
    d = Distrib([joueur])
    d.distribuer_mains()
    d.distribuer_turn()
    # Le turn ne doit pas être distribué
    assert d.turn is None
    assert d.tour_actuel == "preflop"


def test_distribuer_river_un_joueur():
    joueur = Joueur("Solo", 1000)
    d = Distrib([joueur])
    d.distribuer_mains()
    d.distribuer_river()
    # La river ne doit pas être distribuée
    assert d.river is None
    assert d.tour_actuel == "preflop"
