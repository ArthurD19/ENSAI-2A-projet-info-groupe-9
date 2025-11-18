from src.dao.statistique_dao import StatistiqueDao

from src.utils.log_decorator import log


class StatistiqueService:
    @log
    def afficher_statistiques_joueur(self, pseudo):
        """
        Renvoie toutes les statistiques d'un joueur
        """
        return StatistiqueDao().trouver_statistiques_par_id(pseudo)
