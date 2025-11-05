import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection


class StatistiqueDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Statistiques des joueurs de la 
       base de données"""

    CHAMPS_AUTORISES = {
        "meilleur_classement",
        "nombre_total_mains_jouees",
        "nombre_mains_jouees_session",
        "nombre_all_in",
        "nombre_folds",
        "nombre_mises",
        "nombre_relances",
        "nombre_suivis",
        "nombre_checks"
    }

    def creer_statistiques_pour_joueur(self, pseudo: str):
        """Crée une nouvelle ligne de statistiques pour un joueur dans la base de données.
        
        Parameters
        ----------
        pseudo: str
            pseudo du joueur que l'on souhaite ajouter dans la base de données, dans la table player_stats"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO joueurs_statistiques (pseudo) 
                        VALUES (%(pseudo)s)
                        ON CONFLICT (pseudo) DO NOTHING;
                        """,
                        {"pseudo": pseudo},
                    )
        except Exception as e:
            logging.info(e)
            raise

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
                        "  FROM joueurs_statistiques                      "
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
            if statistiques["nombre_total_mains_jouees"] != 0:
                statistiques["taux_main_all_in"] = statistiques["nombre_all_in"]/statistiques["nombre_total_mains_jouees"]
                statistiques["taux_main_fold"] = statistiques["nombre_folds"]/statistiques["nombre_total_mains_jouees"]
                # il reste type_joueur_selon_frequence_jeux
                statistiques["agression_factor"] = (statistiques["nombre_mises"] + statistiques["nombre_relances"])/statistiques["nombre_suivis"]
                statistiques["agression_frequency"] = (statistiques["nombre_mises"] + statistiques["nombre_relances"])/(statistiques["nombre_suivis"] + statistiques["nombre_checks"] + statistiques["nombre_folds"] + statistiques["nombre_relances"] + statistiques["nombre_mises"])
                if statistiques["taux_main_all_in"] > 0.3:
                    statistiques["badge"] = "Le mitrailleur"
                elif statistiques["taux_main_fold"] > 0.45:
                    statistiques["badge"] = "Gérard j'ai pas les bonnes cartes"
                elif statistiques["agression_factor"] >= 3.5 and statistiques["agression_frequency"] >= 0.55:
                    statistiques["bagde"] = "Bluffeur fou"
                elif 2 <= statistiques["agression_factor"] < 3.5 and 0.3 <= statistiques["agression_frequency"] < 0.55:
                    statistiques["bagde"] = "Agressif"
                elif statistiques["agression_factor"] < 2 and statistiques["agression_frequency"] < 0.3:
                    statistiques["badge"] = "Poule mouillée"
                else:
                    statistiques["badge"] = "Sans badge"
            else:
                statistiques["taux_main_all_in"] = 0
                statistiques["taux_main_fold"] = 0
                statistiques["agression_factor"] = 0
                statistiques["agression_frequency"] = 0
            if statistiques["nombre_fois_abattage"] != 0:
                statistiques["taux_victoire_abattage"] = statistiques["nombre_victoire_abattage"]/statistiques["nombre_fois_abattage"]
            else:
                statistiques["taux_victoire_abattage"] = 0
        return statistiques

    
    def mettre_a_jour_statistique(self, pseudo: str, stat_a_mettre_a_jour: str, valeur: int):
        """Met à jour une statistique spécifique d'un joueur, si le champ est valide.
        
        Parameters
        ----------
        pseudo: str
            pseudo du joueur dont on veut mettre à jour une statistique
        stat_a_mettre_a_jour: str
            nom de la statistique que l'on souhaite mettre à jour
        valeur: int
            nouvelle valeur de la statistique
        """
        if stat_a_mettre_a_jour not in self.CHAMPS_AUTORISES:
            raise ValueError(f"Champ '{stat_a_mettre_a_jour}' non autorisé pour la mise à jour.")

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    query = f"UPDATE joueurs_statistiques SET {stat_a_mettre_a_jour} = %(valeur)s WHERE pseudo = %(pseudo)s;"
                    cursor.execute(query, {"valeur": valeur, "pseudo": pseudo})
        except Exception as e:
            logging.info(e)
            raise

    def incrementer_statistique(self, pseudo: str, stat_a_incrementer: str, valeur: int = 1):
        """Incrémente une statistique (par exemple +1 main jouée).
        
        Parameters
        ----------
        pseudo: str 
            pseudo du joueur dont on souhaite incrémenter une statistique
        stat_a_incrementer: str
            nom de la statistique que l'on souhaite incrementer
        valeur: int
            valeur dont on souhaite augmenter la statistique, par défaut vaut 1"""
        if stat_a_incrementer not in self.CHAMPS_AUTORISES:
            raise ValueError(f"Champ '{stat_a_incrementer}' non autorisé pour la mise à jour.")
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    query = f"UPDATE joueurs_statistiques SET {stat_a_incrementer} = {stat_a_incrementer} + %(valeur)s WHERE pseudo = %(pseudo)s;"
                    cursor.execute(query, {"valeur": valeur, "pseudo": pseudo})
        except Exception as e:
            logging.info(e)
            raise

    
    def recuperer_top_joueurs(self, limite: int = 10) -> list[dict]:
        """Renvoie la liste des meilleurs joueurs selon leur meilleur classement.
        
        Parameters
        ----------
        limite: int
            nombre de top joueur que l'on souhaite renvoyer
            
        Return
        ------
        dict ou list"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT pseudo, meilleur_classement
                        FROM joueurs_statistiques
                        WHERE meilleur_classement IS NOT NULL
                        ORDER BY meilleur_classement ASC
                        LIMIT %(limite)s;
                        """,
                        {"limite": limite},
                    )
                    res = cursor.fetchall()
            return res or []
        except Exception as e:
            logging.info(e)
            raise
