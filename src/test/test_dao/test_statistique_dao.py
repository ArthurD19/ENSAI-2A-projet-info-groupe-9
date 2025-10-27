import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.statistique_dao import StatistiqueDao
from dao.joueur_dao import JoueurDao


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Prépare un environnement de test isolé 
    """
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_statistiques_par_id_existant():
    """
    Récupération des statistiques d'un joueur existant (le joueur existe dans la base de données)
    """
    # GIVEN
    pseudo = "clemence"  # joueur déjà présent dans la base de test
    # WHEN
    stats = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    # THEN
    assert isinstance(stats, dict)
    assert "nombre_total_mains_jouees" in stats
    assert "taux_main_all_in" in stats
    assert stats["pseudo"] == pseudo


def test_trouver_statistiques_par_id_inexistant():
    """
    Lecture d'un pseudo inexistant dans la base de données
    """
    # GIVEN
    pseudo = "inconnu"
    # WHEN
    stats = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    # THEN
    assert stats == {}


from dao.joueur_dao import JoueurDao


def test_creer_statistiques_pour_joueur_ok():
    """
    Création de statistiques réussie pour un joueur
    """
    # GIVEN
    joueur = {
        "pseudo": "nouveau_joueur",
        "mdp": "mdp",
        "portefeuille": None,
        "code_parrainage": None
    }
    # WHEN
    JoueurDao().creer(joueur)
    StatistiqueDao().creer_statistiques_pour_joueur(joueur["pseudo"])
    # THEN
    stats = StatistiqueDao().trouver_statistiques_par_id(joueur["pseudo"])
    assert stats is not None
    assert stats["pseudo"] == joueur["pseudo"]

# est ce qu'il faut faire le test dans le cas où ça ne marche pas car le joueur n'existe pas dans la base de données

def test_mettre_a_jour_statistique_ok():
    """
    Mise à jour d'une valeur puis vérification que la mise à jour s'est faite correctement
    """
    #GIVEN
    pseudo = "arthur"
    stat_a_mettre_a_jour = "nombre_folds"
    nouvelle_valeur = 22
    # WHEN
    StatistiqueDao().mettre_a_jour_statistique(pseudo, stat_a_mettre_a_jour, nouvelle_valeur)
    stats = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    # THEN 
    assert stats[stat_a_mettre_a_jour] == nouvelle_valeur


def test_mettre_a_jour_statistique_non_autorisee():
    """
    Erreur si on tente de mettre à jour une statistique qui n'existe pas
    """
    # GIVEN
    pseudo = "lucas"
    # THEN
    with pytest.raises(ValueError):
        StatistiqueDao().mettre_a_jour_statistique("lucas", "stat_inconnue", 10)

def test_incrementer_statistique_valeur_par_defaut_ok():
    """
    Incrémentation d'une statistique puis vérification que l'incrémentation s'est faite correctement
    """
    # GIVEN
    pseudo = "maxence"
    stat_a_incrementer = "nombre_mises"
    # WHEN
    stats_avant = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    val_avant = stats_avant[stat_a_incrementer]
    StatistiqueDao().incrementer_statistique(pseudo, stat_a_incrementer)
    stats_apres = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    # THEN 
    assert stats_apres[stat_a_incrementer] == val_avant + 1


def test_incrementer_statistique_valeur_autre_ok():
    """
    Incrémentation d'une statistique puis vérification que l'incrémentation s'est faite correctement
    """
    # GIVEN
    pseudo = "maxence"
    stat_a_incrementer = "nombre_mises"
    valeur = 5
    # WHEN 
    stats_avant = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    val_avant = stats_avant[stat_a_incrementer]
    StatistiqueDao().incrementer_statistique(pseudo, stat_a_incrementer, valeur)
    stats_apres = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    # THEN
    assert stats_apres[stat_a_incrementer] == val_avant + valeur


def test_incrementer_statistique_champ_non_autorise():
    """
    Erreur si on tente d'incrémenter une statistique inconnue ou non autorisee
    """
    # GIVEN
    pseudo = "lucas"
    # THEN
    with pytest.raises(ValueError):
        StatistiqueDao().incrementer_statistique(pseudo, "stat_inconnue", 1)