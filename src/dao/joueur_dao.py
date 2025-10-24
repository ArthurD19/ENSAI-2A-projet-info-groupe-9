import logging
import psycopg2
import psycopg2.extras
from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection



class JoueurDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    @log
    def creer(self, joueur: dict) -> bool:
        """
        Création d'un joueur dans la base de données

        joueur : dict
            Exemple :
            {
                "pseudo": "Alice",
                "mdp": "motdepasse123",
                "portefeuille": 1000,
                "code_parrainage": "ABC12"
            }

        Retourne True si succès, False sinon
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO players (pseudo, mdp, portefeuille, code_parrainage)
                        VALUES (%(pseudo)s, %(mdp)s, %(portefeuille)s, %(code_parrainage)s);
                        """,
                        joueur,
                    )
            return True
        except Exception as e:
            logging.exception(e)
            return False

    # --------------------------------------------------------------------------

    @log
    def trouver_par_pseudo(self, pseudo: str) -> dict | None:
        """Trouver un joueur grâce à son pseudo"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT pseudo, mdp, portefeuille, code_parrainage
                        FROM players
                        WHERE pseudo = %(pseudo)s;
                        """,
                        {"pseudo": pseudo},
                    )
                    return cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            return None

    # --------------------------------------------------------------------------

    @log
    def lister_tous(self) -> list[dict]:
        """Lister tous les joueurs de la base"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT pseudo, mdp, portefeuille, code_parrainage
                        FROM players;
                        """
                    )
                    return cursor.fetchall() or []
        except Exception as e:
            logging.exception(e)
            return []

    # --------------------------------------------------------------------------

    @log
    def modifier(self, joueur: dict) -> bool:
        """Modifier les informations d'un joueur dans la base"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE players
                           SET mdp = %(mdp)s,
                               portefeuille = %(portefeuille)s,
                               code_parrainage = %(code_parrainage)s
                         WHERE pseudo = %(pseudo)s;
                        """,
                        joueur,
                    )
                    return cursor.rowcount == 1
        except Exception as e:
            logging.exception(e)
            return False

    # --------------------------------------------------------------------------

    @log
    def supprimer(self, pseudo: str) -> bool:
        """Supprimer un joueur grâce à son pseudo"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM players WHERE pseudo = %(pseudo)s;",
                        {"pseudo": pseudo},
                    )
                    return cursor.rowcount > 0
        except Exception as e:
            logging.exception(e)
            return False

    # --------------------------------------------------------------------------

    @log
    def se_connecter(self, pseudo: str, mdp: str) -> dict | None:
        """
        Vérifie si un joueur existe avec ce pseudo et ce mot de passe exact.
        Retourne un dict avec pseudo, mdp, portefeuille, code_parrainage
        ou None si aucun joueur trouvé.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                    cursor.execute(
                        """
                        SELECT pseudo, mdp, portefeuille, code_parrainage
                        FROM players
                        WHERE pseudo = %(pseudo)s
                          AND mdp = %(mdp)s;
                        """,
                        {"pseudo": pseudo, "mdp": mdp},
                    )
                    res = cursor.fetchone()
                    return dict(res) if res else None
        except Exception as e:
            logging.exception(e)
            return None


    # --------------------------------------------------------------------------

    @log
    def valeur_portefeuille(self, pseudo: str) -> int | None:
        """Renvoie la valeur du portefeuille pour un joueur donné"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT portefeuille
                        FROM players
                        WHERE pseudo = %(pseudo)s;
                        """,
                        {"pseudo": pseudo},
                    )
                    res = cursor.fetchone()
                    return res["portefeuille"] if res else None
        except Exception as e:
            logging.exception(e)
            return None

    # --------------------------------------------------------------------------

    @log
    def classement_par_portefeuille(self, limit: int | None = None) -> list[dict]:
        """
        Retourne le classement des joueurs selon la valeur de leur portefeuille (desc)
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if limit:
                        cursor.execute(
                            """
                            SELECT pseudo, portefeuille
                            FROM players
                            ORDER BY portefeuille DESC
                            LIMIT %(limit)s;
                            """,
                            {"limit": limit},
                        )
                    else:
                        cursor.execute(
                            """
                            SELECT pseudo, portefeuille
                            FROM players
                            ORDER BY portefeuille DESC;
                            """
                        )
                    return cursor.fetchall() or []
        except Exception as e:
            logging.exception(e)
            return []

    # --------------------------------------------------------------------------

    @log
    def code_de_parrainage_existe(self, code: str) -> bool:
        """Vérifie si un code de parrainage existe déjà"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 1
                        FROM players
                        WHERE code_parrainage = %(code)s
                        LIMIT 1;
                        """,
                        {"code": code},
                    )
                    return cursor.fetchone() is not None
        except Exception as e:
            logging.exception(e)
            return False

    # --------------------------------------------------------------------------

    @log
    def mettre_a_jour_code_de_parrainage(self, pseudo: str, nouveau_code: str) -> bool:
        """Met à jour le code de parrainage pour un joueur donné"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE players
                        SET code_parrainage = %(nouveau_code)s
                        WHERE pseudo = %(pseudo)s;
                        """,
                        {"pseudo": pseudo, "nouveau_code": nouveau_code},
                    )
                    return cursor.rowcount == 1
        except Exception as e:
            logging.exception(e)
            return False
