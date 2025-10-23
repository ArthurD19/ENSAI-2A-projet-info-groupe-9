import os
import pytest
from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password
from dao.joueur_dao import JoueurDao


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


# --------------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------------

def test_trouver_par_id_existant():
    """Recherche par id d'un joueur existant"""

    # GIVEN
    id_joueur = 998

    # WHEN
    joueur = JoueurDao().trouver_par_id(id_joueur)

    # THEN
    assert joueur is not None
    assert isinstance(joueur, dict)
    assert joueur["id_joueur"] == id_joueur


def test_trouver_par_id_non_existant():
    """Recherche par id d'un joueur n'existant pas"""

    # GIVEN
    id_joueur = 9999999999999

    # WHEN
    joueur = JoueurDao().trouver_par_id(id_joueur)

    # THEN
    assert joueur is None


def test_lister_tous():
    """Vérifie que la méthode renvoie une liste de joueurs (dict)"""

    # GIVEN
    # Aucun prérequis particulier

    # WHEN
    joueurs = JoueurDao().lister_tous()

    # THEN
    assert isinstance(joueurs, list)
    for j in joueurs:
        assert isinstance(j, dict)
        assert "pseudo" in j
        assert "portefeuille" in j
    assert len(joueurs) >= 2


def test_creer_ok():
    """Création de joueur réussie"""

    # GIVEN
    joueur = {
        "pseudo": "gg",
        "mdp": hash_password("motdepasse", "gg"),
        "portefeuille": 1000,
        "code_de_parrainage": "TEST123",
    }

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert creation_ok
    assert "id_joueur" in joueur
    assert isinstance(joueur["id_joueur"], int)


def test_creer_ko():
    """Création de joueur échouée (champ manquant ou invalide)"""

    # GIVEN
    joueur = {
        "pseudo": None,
        "mdp": "vide",
        "portefeuille": None,
        "code_de_parrainage": None,
    }

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert not creation_ok


def test_modifier_ok():
    """Modification de joueur réussie"""

    # GIVEN
    joueur = {
        "id_joueur": 997,
        "pseudo": "maurice",
        "mdp": hash_password("9876", "maurice"),
        "portefeuille": 2000,
        "code_de_parrainage": "MAU123",
    }

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert modification_ok


def test_modifier_ko():
    """Modification échouée (id inconnu)"""

    # GIVEN
    joueur = {
        "id_joueur": 888888,
        "pseudo": "id inconnu",
        "mdp": "inexistant",
        "portefeuille": 10,
        "code_de_parrainage": "XXX000",
    }

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression de joueur réussie"""

    # GIVEN
    joueur = {
        "pseudo": "miguel",
        "mdp": hash_password("mdp", "miguel"),
        "portefeuille": 500,
        "code_de_parrainage": "DEL123",
    }
    JoueurDao().creer(joueur)

    # WHEN
    suppression_ok = JoueurDao().supprimer(joueur["id_joueur"])

    # THEN
    assert suppression_ok


def test_supprimer_ko():
    """Suppression échouée (id inconnu)"""

    # GIVEN
    id_inconnu = 999999999

    # WHEN
    suppression_ok = JoueurDao().supprimer(id_inconnu)

    # THEN
    assert not suppression_ok


def test_se_connecter_ok():
    """Connexion de joueur réussie"""

    # GIVEN
    pseudo = "batricia"
    mdp = "9876"
    hashed = hash_password(mdp, pseudo)

    # WHEN
    joueur = JoueurDao().se_connecter(pseudo, hashed)

    # THEN
    assert joueur is not None
    assert isinstance(joueur, dict)
    assert joueur["pseudo"] == pseudo


def test_se_connecter_ko():
    """Connexion échouée (pseudo ou mdp incorrect)"""

    # GIVEN
    pseudo = "toto"
    mdp = "fauxmdp"
    hashed = hash_password(mdp, pseudo)

    # WHEN
    joueur = JoueurDao().se_connecter(pseudo, hashed)

    # THEN
    assert joueur is None


if __name__ == "__main__":
    pytest.main([__file__])
