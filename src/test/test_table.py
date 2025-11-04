import pytest
from business_object.cartes import Deck
from business_object.joueurs import Joueur
from business_object.table import Table


@pytest.fixture
def table_vide():
    """Crée une table vide pour les tests."""
    return Table(id=1, blind=20)


@pytest.fixture
def joueurs():
    """Crée deux joueurs pour les tests."""
    return Joueur("Alice", 1000), Joueur("Bob", 1000)


def test_initialisation_table(table_vide):
    """Vérifie que la table s'initialise correctement."""
    assert table_vide.id == 1
    assert table_vide.blind == 20
    assert table_vide.pot == 0
    assert table_vide.joueurs == []
    assert isinstance(table_vide.deck, Deck)
    assert table_vide.board == []


def test_ajouter_joueur(table_vide, joueurs):
    """Ajoute un joueur et vérifie qu'il est bien présent."""
    alice, _ = joueurs
    table_vide.ajouter_joueur(alice)
    assert alice in table_vide.joueurs
    assert len(table_vide.joueurs) == 1


def test_ajouter_joueur_deja_present(table_vide, joueurs):
    """Vérifie qu'on ne peut pas ajouter deux fois le même joueur."""
    alice, _ = joueurs
    table_vide.ajouter_joueur(alice)
    with pytest.raises(ValueError):
        table_vide.ajouter_joueur(alice)


def test_supprimer_joueur(table_vide, joueurs):
    """Supprime un joueur et vérifie qu'il est bien retiré."""
    alice, _ = joueurs
    table_vide.ajouter_joueur(alice)
    table_vide.supprimer_joueur(alice)
    assert alice not in table_vide.joueurs
    assert len(table_vide.joueurs) == 0


def test_supprimer_joueur_inexistant(table_vide, joueurs):
    """Vérifie qu'on ne peut pas retirer un joueur non présent."""
    alice, _ = joueurs
    with pytest.raises(ValueError):
        table_vide.supprimer_joueur(alice)


def test_reset_table(table_vide, joueurs):
    """Vérifie que reset_table vide bien la table et recrée un Deck."""
    alice, _ = joueurs
    table_vide.ajouter_joueur(alice)
    table_vide.pot = 100
    table_vide.board = [1, 2, 3]
    ancien_deck = table_vide.deck

    table_vide.reset_table()

    assert table_vide.pot == 0
    assert table_vide.board == []
    assert isinstance(table_vide.deck, Deck)
    assert table_vide.deck is not ancien_deck  # le deck a bien été recréé


def test_repr(table_vide, joueurs):
    """Teste la représentation textuelle de la table."""
    alice, bob = joueurs
    table_vide.ajouter_joueur(alice)
    table_vide.ajouter_joueur(bob)
    rep = repr(table_vide)
    assert "Table 1" in rep
    assert "Alice" in rep
    assert "Bob" in rep
