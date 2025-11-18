import pytest
from unittest.mock import patch
from src.view.menu_joueur_vue import MenuJoueurVue
from src.view.menu_rejoindre_table_vue import MenuRejoindreTableVue
from src.view.menu_table_vue import MenuTableVue
from src.view.accueil.accueil_vue import AccueilVue


# ---------------------- TESTS POUR MenuJoueurVue ----------------------

@pytest.fixture
def vue():
    return MenuJoueurVue("Titre Test", tables=["Table1", "Table2"])


def test_instanciation_vue(vue):
    assert vue.message == "Titre Test"
    assert isinstance(vue, MenuJoueurVue)


@patch("src.view.menu_joueur_vue.inquirer.select")
@patch("src.view.menu_joueur_vue.Session")
@patch("src.view.menu_joueur_vue.JoueurService")
def test_se_deconnecter(mock_service, mock_session, mock_inquirer, vue):
    mock_inquirer.return_value.execute.return_value = "Se déconnecter"
    mock_session.return_value.joueur = "test_pseudo"
    mock_service.return_value.se_deconnecter.return_value = True

    result = vue.choisir_menu()
    assert "AccueilVue" in str(type(result))


@patch("builtins.input", return_value="")
@patch("src.view.menu_joueur_vue.inquirer.select")
@patch("src.view.menu_joueur_vue.get")
@patch("src.view.menu_joueur_vue.Session")
def test_afficher_portefeuille(mock_session, mock_get, mock_inquirer, mock_input, vue, capsys):
    mock_inquirer.return_value.execute.return_value = "Afficher la valeur du portefeuille"
    mock_session.return_value.joueur = "test_pseudo"
    mock_get.return_value = 500

    result = vue.choisir_menu()
    captured = capsys.readouterr()
    assert "Votre portefeuille contient : 500 jetons" in captured.out
    assert isinstance(result, MenuJoueurVue)


@patch("builtins.input", return_value="")
@patch("src.view.menu_joueur_vue.inquirer.select")
@patch("src.view.menu_joueur_vue.get")
@patch("src.view.menu_joueur_vue.Session")
def test_afficher_classement(mock_session, mock_get, mock_inquirer, mock_input, vue, capsys):
    mock_inquirer.return_value.execute.return_value = "Afficher le classement"
    mock_session.return_value.joueur = "test_pseudo"
    mock_get.return_value = [
        {"pseudo": "test_pseudo", "portefeuille": 1000},
        {"pseudo": "autre", "portefeuille": 500},
    ]

    result = vue.choisir_menu()
    captured = capsys.readouterr()
    assert "Classement des joueurs" in captured.out
    assert "test_pseudo" in captured.out
    assert isinstance(result, MenuJoueurVue)


# ---------------------- TESTS POUR MenuRejoindreTableVue ----------------------

@pytest.fixture
def vue_rejoindre():
    return MenuRejoindreTableVue("Message Test")


@patch("builtins.input", return_value="")
@patch("src.view.menu_rejoindre_table_vue.get")
@patch("src.view.menu_rejoindre_table_vue.Session")
def test_aucune_table(mock_session, mock_get, mock_input, vue_rejoindre, capsys):
    mock_session.return_value.joueur = "test_pseudo"
    mock_get.return_value = []

    result = vue_rejoindre.choisir_menu()
    captured = capsys.readouterr()
    assert "Aucune table disponible" in captured.out
    assert isinstance(result, MenuJoueurVue)


@patch("builtins.input", return_value="")
@patch("src.view.menu_rejoindre_table_vue.inquirer.select")
@patch("src.view.menu_rejoindre_table_vue.get")
@patch("src.view.menu_rejoindre_table_vue.Session")
def test_retour_choix(mock_session, mock_get, mock_inquirer, mock_input, vue_rejoindre):
    mock_session.return_value.joueur = "test_pseudo"
    mock_get.return_value = [{"id": 1, "nb_joueurs": 3}]
    mock_inquirer.return_value.execute.return_value = "Retour"

    result = vue_rejoindre.choisir_menu()
    assert isinstance(result, MenuJoueurVue)


@patch("builtins.input", return_value="")
@patch("src.view.menu_rejoindre_table_vue.inquirer.select")
@patch("src.view.menu_rejoindre_table_vue.post")
@patch("src.view.menu_rejoindre_table_vue.get")
@patch("src.view.menu_rejoindre_table_vue.Session")
def test_rejoindre_table(mock_session, mock_get, mock_post, mock_inquirer, mock_input, vue_rejoindre, capsys):
    mock_session.return_value.joueur = "test_pseudo"
    mock_get.return_value = [{"id": 2, "nb_joueurs": 4}]
    mock_inquirer.return_value.execute.return_value = "2 (joueurs: 4)"
    mock_post.return_value = "Vous avez rejoint la table !"

    result = vue_rejoindre.choisir_menu()
    captured = capsys.readouterr()
    assert "Vous avez rejoint la table !" in captured.out
    assert isinstance(result, MenuTableVue)


# ---------------------- TESTS POUR MenuTableVue ----------------------

@pytest.fixture
def vue_table():
    return MenuTableVue(message="En jeu", id_table=1)


@patch("src.view.menu_table_vue.get")
def test_afficher_etat_partie(mock_get, vue_table, capsys):
    mock_get.return_value = {
        "joueur_courant": "test_pseudo",
        "tour_actuel": "Flop",
        "pot": 100,
        "mise_max": 20,
        "joueurs": [
            {"pseudo": "test_pseudo", "solde": 500, "mise": 10, "actif": True},
            {"pseudo": "autre", "solde": 300, "mise": 20, "actif": False},
        ],
        "board": ["As", "Roi", "Dame"],
        "finie": False
    }

    etat = vue_table.afficher_etat_partie()
    captured = capsys.readouterr()
    assert "Table 1" in captured.out
    assert "Flop" in captured.out
    assert etat["pot"] == 100

