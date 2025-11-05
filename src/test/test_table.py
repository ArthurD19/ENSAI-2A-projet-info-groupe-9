import pytest
from business_object.joueurs import Joueur
from business_object.table import Table


@pytest.fixture
def table_vide():
    return Table(id=1, blind=10)

@pytest.fixture
def joueurs():
    return [Joueur(f"Joueur{i+1}", 1000) for i in range(6)]

def test_ajouter_joueur_codes(table_vide, joueurs):
    # Ajouter premier joueur
    result = table_vide.ajouter_joueur(joueurs[0])
    assert result == 1
    # Ajouter même joueur à nouveau
    result = table_vide.ajouter_joueur(joueurs[0])
    assert result == 2
    # Ajouter 4 autres joueurs
    for j in joueurs[1:5]:
        result = table_vide.ajouter_joueur(j)
        assert result == 1
    # Table pleine, ajout du 6ème
    result = table_vide.ajouter_joueur(joueurs[5])
    assert result == 3

def test_supprimer_joueur(table_vide, joueurs):
    alice = joueurs[0]
    # ajouter avant de supprimer
    table_vide.ajouter_joueur(alice)
    table_vide.supprimer_joueur(alice)
    assert alice not in table_vide.joueurs
    assert len(table_vide.joueurs) == 0


def test_reset_table(table_vide, joueurs):
    alice = joueurs[0]
    table_vide.ajouter_joueur(alice)
    table_vide.pot = 100
    table_vide.board = [1, 2, 3]
    ancien_deck = table_vide.deck

    table_vide.reset_table()

    assert table_vide.pot == 0
    assert table_vide.board == []
    assert table_vide.deck is not ancien_deck


def test_repr(table_vide, joueurs):
    for j in joueurs[:3]:
        table_vide.ajouter_joueur(j)
    rep = repr(table_vide)
    assert f"Table {table_vide.id}" in rep
    for j in joueurs[:3]:
        assert j.pseudo in rep
