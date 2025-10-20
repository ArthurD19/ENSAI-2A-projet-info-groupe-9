import os
import pytest

from unittest.mock import patch

from utils.reset_database import ResetDatabase
from utils.securite import hash_password

from dao.statistique_dao import StatistiqueDao


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Prépare un environnement de test isolé 
    """
    with patch.dict(os.environ, {"SCHEMA": "projet_test_dao"}):
        # ResetDatabase pas encore codée
        ResetDatabase().lancer(test_dao=True)
        yield


def test_trouver_statistiques_par_id_existant():
    """Récupération des statistiques d'un joueur existant"""
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
    """Lecture d'un pseudo inexistant"""
    # GIVEN
    pseudo = "inconnu"
    # WHEN
    stats = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    # THEN
    assert stats == {}


def test_creer_statistiques_pour_joueur_ok():
    """Création de statistiques réussie pour un joueur"""
    # GIVEN
    pseudo = "nouveau_joueur"
    # WHEN
    StatistiqueDao().creer_statistiques_pour_joueur(pseudo)
    # THEN
    stats = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    assert stats is not None
    assert stats["pseudo"] == pseudo



def test_mettre_a_jour_statistique_ok():
    """Mise à jour d'une valeur puis vérification"""
    pseudo = "arthur"
    champ = "nombre_folds"
    nouvelle_valeur = 22

    StatistiqueDao().mettre_a_jour_statistique(pseudo, champ, nouvelle_valeur)
    stats = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    assert stats[champ] == nouvelle_valeur


def test_mettre_a_jour_statistique_champ_non_autorise():
    """Erreur si on tente de mettre à jour un champ non autorisé"""
    # GIVEN
    pseudo = "batricia"
    # THEN
    with pytest.raises(ValueError):
        StatistiqueDao().mettre_a_jour_statistique(pseudo, "champ_invalide", 10)


def test_incrementer_statistique_ok():
    """Incrémentation puis vérification"""
    pseudo = "maxence"
    champ = "nombre_mises"

    stats_avant = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    val_avant = stats_avant[champ]

    StatistiqueDao().incrementer_statistique(pseudo, champ)
    stats_apres = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    assert stats_apres[champ] == val_avant + 1