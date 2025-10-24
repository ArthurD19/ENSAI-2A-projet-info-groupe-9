import os
import uuid
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


# --------------------------------------------------------------------------
# NOUVEAUX TESTS pour les méthodes ajoutées
# --------------------------------------------------------------------------

def test_valeur_portefeuille_existant():
    """Renvoie la valeur du portefeuille pour un joueur existant"""

    # GIVEN
    id_joueur = 998  # joueur présent dans la DB de test

    # WHEN
    valeur = JoueurDao().valeur_portefeuille(id_joueur)

    # THEN
    assert valeur is not None
    assert isinstance(valeur, (int, float))


def test_valeur_portefeuille_non_existant():
    """None pour un id de joueur qui n'existe pas"""

    # GIVEN
    id_joueur = 9999999999999

    # WHEN
    valeur = JoueurDao().valeur_portefeuille(id_joueur)

    # THEN
    assert valeur is None


def test_classement_par_portefeuille():
    """Vérifie le classement décroissant par portefeuille"""

    # WHEN
    classement = JoueurDao().classement_par_portefeuille()

    # THEN
    assert isinstance(classement, list)
    # Au moins deux joueurs pour vérifier l'ordre
    assert len(classement) >= 2
    # Vérifier la forme et l'ordre décroissant
    valeurs = []
    for item in classement:
        assert isinstance(item, dict)
        assert "id_joueur" in item
        assert "pseudo" in item
        assert "portefeuille" in item
        valeurs.append(item["portefeuille"])
    assert valeurs == sorted(valeurs, reverse=True)


def test_classement_par_portefeuille_limite():
    """Vérifie que la limite fonctionne"""

    # WHEN
    classement_limit = JoueurDao().classement_par_portefeuille(limit=2)

    # THEN
    assert isinstance(classement_limit, list)
    assert len(classement_limit) <= 2


def test_code_de_parrainage_existe_et_non_existe():
    """Vérifie la détection de l'existence d'un code de parrainage"""

    code = "EXISTE123"
    joueur = {
        "pseudo": "pierre",
        "mdp": hash_password("mdp", "pierre"),
        "portefeuille": 0,
        "code_de_parrainage": code,
    }
    JoueurDao().creer(joueur)

    assert JoueurDao().code_de_parrainage_existe(code) is True
    assert JoueurDao().code_de_parrainage_existe("INEXISTANT999") is False


def test_mettre_a_jour_code_de_parrainage():
    """Met à jour le code de parrainage d’un joueur"""

    joueur = {
        "pseudo": "jean",
        "mdp": hash_password("mdp", "jean"),
        "portefeuille": 0,
        "code_de_parrainage": "OLD001",
    }
    JoueurDao().creer(joueur)
    id_joueur = joueur["id_joueur"]

    nouveau_code = "NEW001"
    maj_ok = JoueurDao().mettre_a_jour_code_de_parrainage(id_joueur, nouveau_code)

    assert maj_ok is True
    assert JoueurDao().code_de_parrainage_existe(nouveau_code) is True
    assert JoueurDao().code_de_parrainage_existe("OLD001") is False


if __name__ == "__main__":
    pytest.main([__file__])