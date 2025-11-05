import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase

from dao.table_dao import TableDao


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Prépare un environnement de test isolé 
    """
    with patch.dict(os.environ, {"POSTGRES_SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer()
        yield


def test_obtenir_joueurs_table_ok():
    """
    Récupération des joueurs dans une table
    """
    # GIVEN
    id_table = 1
    # WHEN
    joueurs_table = TableDao().obtenir_joueurs_tables(id_table)
    # THEN
    assert joueurs_table is not None
    assert joueurs_table["joueur1"] == "clemence"


