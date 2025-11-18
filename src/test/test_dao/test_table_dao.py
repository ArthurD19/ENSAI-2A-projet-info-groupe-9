# src/test/test_table_dao.py
import pytest
from unittest.mock import MagicMock, patch

from src.dao.table_dao import TableDao


@pytest.fixture
def dao():
    return TableDao()


def test_obtenir_joueurs_tables_ok(dao):
    # Mock DBConnection et curseur
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = {"joueur1": "Alice", "joueur2": "Bob"}
    mock_connection = MagicMock()
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
    
    with patch("src.dao.table_dao.DBConnection") as mock_db:
        mock_db.return_value.connection.__enter__.return_value = mock_connection

        result = dao.obtenir_joueurs_tables(1)

        # Vérifie que le curseur a été utilisé pour exécuter la requête
        mock_cursor.execute.assert_called_once()
        assert result == {"joueur1": "Alice", "joueur2": "Bob"}


def test_obtenir_joueurs_tables_exception(dao):
    # Simuler une exception lors de l'accès à la DB
    with patch("src.dao.table_dao.DBConnection") as mock_db:
        mock_db.return_value.connection.__enter__.side_effect = Exception("DB error")
        with pytest.raises(Exception, match="DB error"):
            dao.obtenir_joueurs_tables(1)

