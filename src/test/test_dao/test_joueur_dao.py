import os
import pytest
from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password
from dao.joueur_dao import JoueurDao
from dao.db_connection import DBConnection



@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Initialisation des données de test"""
    with patch.dict(os.environ, {"POSTGRES_SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


# --------------------------------------------------------------------------
# TESTS
# --------------------------------------------------------------------------
def test_verifier_joueurs_existent():
    """Vérifie que la table players contient bien les joueurs attendus"""
    
    # GIVEN / WHEN
    with DBConnection().connection as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pseudo, mdp, portefeuille, code_parrainage FROM players;")
            joueurs = cursor.fetchall()
            print("Joueurs présents dans la DB:", joueurs)
    
    # THEN
    assert len(joueurs) > 0
    pseudos = [j['pseudo'] for j in joueurs]
    assert "arthur" in pseudos


def test_trouver_par_pseudo_existant():
    """Recherche par pseudo d'un joueur existant"""
    # GIVEN
    pseudo = "arthur"

    # WHEN
    joueur = JoueurDao().trouver_par_pseudo(pseudo)

    # THEN
    assert joueur is not None
    assert isinstance(joueur, dict)
    assert joueur["pseudo"] == pseudo


def test_trouver_par_pseudo_non_existant():
    """Recherche par pseudo d'un joueur n'existant pas"""
    # GIVEN
    pseudo = "pseudo_inexistant"

    # WHEN
    joueur = JoueurDao().trouver_par_pseudo(pseudo)

    # THEN
    assert joueur is None


def test_lister_tous():
    """Vérifie que la méthode renvoie une liste de joueurs (dict)"""
    # GIVEN
    expected_pseudos = ["arthur", "maxence", "lucas", "clemence"]

    # WHEN
    joueurs = JoueurDao().lister_tous()

    # THEN
    assert isinstance(joueurs, list)
    pseudos = [j["pseudo"] for j in joueurs]
    for pseudo in expected_pseudos:
        assert pseudo in pseudos
    for j in joueurs:
        assert isinstance(j, dict)
        assert "pseudo" in j
        assert "portefeuille" in j


def test_creer_ok():
    """Création de joueur réussie"""
    # GIVEN
    joueur = {
        "pseudo": "gg",
        "mdp": hash_password("motdepasse", "gg"),
        "portefeuille": 1000,
        "code_parrainage": "TES12",
    }

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert creation_ok
    recup = JoueurDao().trouver_par_pseudo("gg")
    assert recup is not None
    assert recup["pseudo"] == "gg"


def test_creer_ko():
    """Création de joueur échouée (champ manquant ou invalide)"""
    # GIVEN
    joueur = {
        "pseudo": None,
        "mdp": "vide",
        "portefeuille": None,
        "code_parrainage": None,
    }

    # WHEN
    creation_ok = JoueurDao().creer(joueur)

    # THEN
    assert not creation_ok


def test_modifier_ok():
    """Modification de joueur réussie"""
    # GIVEN
    joueur = {
        "pseudo": "arthur",
        "mdp": hash_password("nouveau", "arthur"),
        "portefeuille": 2000,
        "code_parrainage": "AAA99",
    }

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert modification_ok
    recup = JoueurDao().trouver_par_pseudo("arthur")
    assert recup["portefeuille"] == 2000
    assert recup["code_parrainage"] == "AAA99"


def test_modifier_ko():
    """Modification échouée (pseudo inconnu)"""
    # GIVEN
    joueur = {
        "pseudo": "pseudo_inexistant",
        "mdp": "inexistant",
        "portefeuille": 10,
        "code_parrainage": "XXX00",
    }

    # WHEN
    modification_ok = JoueurDao().modifier(joueur)

    # THEN
    assert not modification_ok


def test_supprimer_ok():
    """Suppression de joueur réussie"""
    # GIVEN
    joueur = {
        "pseudo": "gg",
        "mdp": hash_password("motdepasse", "gg"),
        "portefeuille": 1000,
        "code_parrainage": "TES12",
    }
    JoueurDao().creer(joueur)

    # WHEN
    suppression_ok = JoueurDao().supprimer("gg")

    # THEN
    assert suppression_ok
    recup = JoueurDao().trouver_par_pseudo("gg")
    assert recup is None


def test_supprimer_ko():
    """Suppression échouée (pseudo inconnu)"""
    # GIVEN
    pseudo_inconnu = "pseudo_inexistant"

    # WHEN
    suppression_ok = JoueurDao().supprimer(pseudo_inconnu)

    # THEN
    assert not suppression_ok


def test_se_connecter_ok():
    pseudo = "arthur"
    mdp = "6aaa410dfb03069e6b3f31e3389c1c666b5db409e96eba06d971630146064bc1"  # avec le truc juste en dessous là jai pu voir le mdp hashé je crois ? donc je l'ai mis directement dans mdp sur la ligne du dessus là mais cest bizarre je pense
    # 👉 Debug : afficher ce qu'il y a vraiment dans la table players
    from dao.db_connection import DBConnection
    with DBConnection().connection as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT pseudo, mdp FROM players;")
            print("DEBUG contenu players:", cur.fetchall())

    # WHEN
    joueur = JoueurDao().se_connecter(pseudo, mdp)

    # THEN
    assert joueur is not None
    assert joueur["pseudo"] == pseudo
    assert joueur["mdp"] == mdp



def test_se_connecter_mauvais_mdp():
    """Connexion échoue si le mot de passe est incorrect"""
    joueur = JoueurDao().se_connecter("arthur", "mauvais_mdp")
    assert joueur is None


def test_se_connecter_inconnu():
    """Connexion échoue si le pseudo n'existe pas"""
    joueur = JoueurDao().se_connecter("inconnu", "hash_mdp_0000")
    assert joueur is None







def test_se_connecter_ko():
    """Connexion échouée (pseudo ou mdp incorrect)"""
    # GIVEN
    pseudo = "arthur"
    mdp = "fauxmdp"
    hashed = hash_password(mdp, pseudo)

    # WHEN
    joueur = JoueurDao().se_connecter(pseudo, hashed)

    # THEN
    assert joueur is None


def test_valeur_portefeuille_existant():
    """Renvoie la valeur du portefeuille pour un joueur existant"""
    # GIVEN
    pseudo = "lucas"

    # WHEN
    valeur = JoueurDao().valeur_portefeuille(pseudo)

    # THEN
    assert valeur is not None
    assert isinstance(valeur, (int, float))


def test_valeur_portefeuille_non_existant():
    """None pour un pseudo qui n'existe pas"""
    # GIVEN
    pseudo = "pseudo_inexistant"

    # WHEN
    valeur = JoueurDao().valeur_portefeuille(pseudo)

    # THEN
    assert valeur is None


def test_classement_par_portefeuille():
    """Vérifie le classement décroissant par portefeuille"""
    # WHEN
    classement = JoueurDao().classement_par_portefeuille()

    # THEN
    assert isinstance(classement, list)
    valeurs = [j["portefeuille"] for j in classement]
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
    # GIVEN
    joueur = {
        "pseudo": "pierre",
        "mdp": hash_password("mdp", "pierre"),
        "portefeuille": 0,
        "code_parrainage": "ZZZ11",
    }
    JoueurDao().creer(joueur)

    # THEN
    assert JoueurDao().code_de_parrainage_existe("ZZZ11") is True
    assert JoueurDao().code_de_parrainage_existe("ZZZ22") is False


def test_mettre_a_jour_code_de_parrainage():
    """Met à jour le code de parrainage d’un joueur"""
    # GIVEN
    joueur = {
        "pseudo": "jean",
        "mdp": hash_password("mdp", "jean"),
        "portefeuille": 0,
        "code_parrainage": "VVV11",
    }
    JoueurDao().creer(joueur)
    pseudo = "jean"

    # WHEN
    nouveau_code = "WWW22"
    maj_ok = JoueurDao().mettre_a_jour_code_de_parrainage(pseudo, nouveau_code)

    # THEN
    assert maj_ok is True
    assert JoueurDao().code_de_parrainage_existe(nouveau_code) is True
    assert JoueurDao().code_de_parrainage_existe("VVV11") is False


if __name__ == "__main__":
    pytest.main([__file__])
