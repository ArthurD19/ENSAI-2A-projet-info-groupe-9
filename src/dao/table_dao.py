import logging

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.db_connection import DBConnection


class TableDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Tables de la 
       base de données"""

    CHAMPS_AUTORISES = {
        "joueur1",
        "joueur2",
        "joueur3",
        "joueur4",
        "joueur5"
    }

    def obtenir_joueurs_tables(self, id: int):
        """Récupère les joueurs qui sont présents à une table.
        
        Parameters
        ----------
        id: int
            identifiant de la table dont on veut connaitre les joueurs"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT *                           "
                        "  FROM table_joueurs                      "
                        " WHERE id = %(id)s;  ",
                        {"id": id},
                    )
                    res = cursor.fetchone()
                    return res
        except Exception as e:
            logging.info(e)
            raise

    def ajouter_joueur_table(self, pseudo: str, id: int):
        """Ajoute le joueur à la table.
        
        Parameters
        ----------
        pseudo: str 
            pseudo du joueur qu'on veut ajouter à une table
        id: int
            identifiant de la table où on veut ajouter le joueur"""
        joueurs_table = self.obtenir_joueurs_tables(id)
        
        
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    query = f"UPDATE table_joueurs SET {joueur} = %(valeur)s WHERE id = %(id)s;"
                    cursor.execute(query, {"pseudo": pseudo, "id": id})
        except Exception as e:
            logging.info(e)
            raisenfo(e)
            raise