import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection

from business_object.joueur import Joueur


class StatistiqueDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Statistiques des joueurs de la 
       base de données"""

    @log
    def trouver_statistiques_par_id(self, pseudo) -> dict[str, int]:
        """renvoie toutes les statistiques d'un joueur

        Parameters
        ----------
        pseudo : str
            pseudo du joueur dont on souhaite renvoyer les statistiques

        Returns
        -------
        statistiques : Dict[str, int]
            dictionnaire contenant toutes les statistiques du joueur
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM player_stats                      "
                        " WHERE pseudo = %(pseudo)s;  ",
                        {"pseudo": pseudo},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.info(e)
            raise

        statistiques = {}
        if res:
            statistiques = res
            statistiques["taux_main_all_in"] = statistiques["nombre_all_in"]/statistiques["nombre_total_mains_jouees"]
            statistiques["taux_main_fold"] = statistiques["nombre_folds"]/statistiques["nombre_total_mains_jouees"]
            # il reste taux_victoire_abattage, type_joueur_selon_frequence_jeux, badge
            statistiques["agression_factor"] = (statistiques["nombre_mises"] + statistiques["nombre_relances"])/statistiques["nombre_suivis"]
            statistiques["agression_frequency"] = (statistiques["nombre_mises"] + statistiques["nombre_relances"])/(statistiques["nombre_suivis"] + statistiques["nombre_checks"] + statistiques["nombre_folds"] + statistiques["nombre_relances"] + statistiques["nombre_mises"])
        return statistiques

    