import pytest
from unittest.mock import patch, MagicMock
import logging
import yaml

from src.utils.genere_code_parrainage import GenerateurDeCode
import src.utils.log_init as log_init


def test_generate_unique_code_not_existing():
    """Vérifie que la fonction retourne un code quand JoueurDao dit qu'il n'existe pas."""

    # Patch du JoueurDao dans le BON module !
    with patch("src.utils.genere_code_parrainage.JoueurDao") as mock_dao:
        mock_dao.return_value.code_de_parrainage_existe.return_value = False

        gen = GenerateurDeCode(length=5)
        code = gen.generate_unique_code()

        assert len(code) == 5
        assert code.isalnum()
        assert code.upper() == code
        mock_dao.return_value.code_de_parrainage_existe.assert_called_once()


def test_generate_unique_code_retry_once():
    """Test : le premier code existe, le second non."""

    with patch("src.utils.genere_code_parrainage.JoueurDao") as mock_dao:
        # simulate : 1er code existe, 2e non
        mock_dao.return_value.code_de_parrainage_existe.side_effect = [True, False]

        # on fixe random.choices pour rendre le test déterministe
        with patch("src.utils.genere_code_parrainage.random.choices") as mock_choices:
            mock_choices.side_effect = [
                list("AAAAA"),  # 1er → existe → retry
                list("BBBBB")   # 2e → OK
            ]

            gen = GenerateurDeCode(length=5)
            code = gen.generate_unique_code()

            assert code == "BBBBB"
            assert mock_choices.call_count == 2
            assert mock_dao.return_value.code_de_parrainage_existe.call_count == 2


def test_initialiser_logs_cree_dossier(monkeypatch):
    # Mock os.makedirs
    makedirs_mock = MagicMock()
    monkeypatch.setattr("os.makedirs", makedirs_mock)

    # Mock open pour le fichier YAML
    open_mock = MagicMock()
    monkeypatch.setattr("builtins.open", lambda *a, **kw: open_mock)

    # Mock yaml.load
    yaml_mock = MagicMock(return_value={"dummy": "config"})
    monkeypatch.setattr(yaml, "load", yaml_mock)

    # Mock logging.config.dictConfig
    dict_config_mock = MagicMock()
    monkeypatch.setattr(logging.config, "dictConfig", dict_config_mock)

    # Mock logging.info
    info_mock = MagicMock()
    monkeypatch.setattr(logging, "info", info_mock)

    # Appel de la fonction
    log_init.initialiser_logs("TestApp")

    # Vérifie que le dossier logs a été créé
    makedirs_mock.assert_called_once_with("logs", exist_ok=True)

    # Vérifie que yaml.load a été appelé
    yaml_mock.assert_called_once()

    # Vérifie que dictConfig a été appelé
    dict_config_mock.assert_called_once_with({"dummy": "config"})

    # Vérifie que logging.info a été appelé pour les lignes de démarrage
    assert info_mock.call_count == 3
    assert any("Lancement TestApp" in str(call) for call in info_mock.call_args_list)