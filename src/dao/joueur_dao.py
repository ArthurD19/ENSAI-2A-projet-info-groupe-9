import logging
from utils.singleton import Singleton
from utils.log_decorator import log
from dao.db_connection import DBConnection


class JoueurDao(metaclass=Singleton):
    """Classe contenant les méthodes pour accéder aux Joueurs de la base de données"""

    @log
    def creer(self, joueur: dict) -> bool:
        """
        Création d'un joueur dans la base de données

        Parameters
        ----------
        joueur : dict
            Exemple :
            {
                "pseudo": "Alice",
                "mdp": "motdepasse123",
                "portefeuille": 1000,
                "code_de_parrainage": "ABC123"
            }

        Returns
        -------
        bool : True si la création est un succès, False sinon
        """
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO joueur (pseudo, mdp, portefeuille, code_de_parrainage)
                        VALUES (%(pseudo)s, %(mdp)s, %(portefeuille)s, %(code_de_parrainage)s)
                        RETURNING id_joueur;
                        """,
                        joueur,
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)

        if res:
            joueur["id_joueur"] = res["id_joueur"]
            return True
        return False

    # --------------------------------------------------------------------------

    @log
    def trouver_par_id(self, id_joueur: int) -> dict | None:
        """Trouver un joueur grâce à son id"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_joueur, pseudo, mdp, portefeuille, code_de_parrainage
                        FROM joueur
                        WHERE id_joueur = %(id_joueur)s;
                        """,
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            return None

        return res  # res est un dict (ou None)

    # --------------------------------------------------------------------------

    @log
    def lister_tous(self) -> list[dict]:
        """Lister tous les joueurs de la base"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_joueur, pseudo, mdp, portefeuille, code_de_parrainage
                        FROM joueur;
                        """
                    )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
            res = []

        return res or []

    # --------------------------------------------------------------------------

    @log
    def modifier(self, joueur: dict) -> bool:
        """Modifier les informations d'un joueur dans la base"""
        res = None

        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE joueur
                           SET pseudo = %(pseudo)s,
                               mdp = %(mdp)s,
                               portefeuille = %(portefeuille)s,
                               code_de_parrainage = %(code_de_parrainage)s
                         WHERE id_joueur = %(id_joueur)s;
                        """,
                        joueur,
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.exception(e)

        return res == 1

    # --------------------------------------------------------------------------

    @log
    def supprimer(self, id_joueur: int) -> bool:
        """Supprimer un joueur grâce à son id"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM joueur WHERE id_joueur = %(id_joueur)s;",
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.rowcount
        except Exception as e:
            logging.exception(e)
            return False

        return res > 0

    # --------------------------------------------------------------------------

    @log
    def se_connecter(self, pseudo: str, mdp: str) -> dict | None:
        """Se connecter grâce à un pseudo et un mot de passe"""
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT id_joueur, pseudo, mdp, portefeuille, code_de_parrainage
                        FROM joueur
                        WHERE pseudo = %(pseudo)s
                          AND mdp = %(mdp)s;
                        """,
                        {"pseudo": pseudo, "mdp": mdp},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            res = None

        return res

    # --------------------------------------------------------------------------

    @log
    def valeur_portefeuille(self, id_joueur: int) -> int | float | None:
        """
        Renvoie la valeur du portefeuille pour un joueur donné.
        Retourne None si le joueur n'existe pas.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT portefeuille
                        FROM joueur
                        WHERE id_joueur = %(id_joueur)s;
                        """,
                        {"id_joueur": id_joueur},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            return None

        if res:
            # res est un dict contenant 'portefeuille'
            return res["portefeuille"]
        return None

    # --------------------------------------------------------------------------

    @log
    def classement_par_portefeuille(self, limit: int | None = None) -> list[dict]:
        """
        Retourne le classement des joueurs selon la valeur de leur portefeuille (desc).
        Si 'limit' est fourni, limite le nombre de résultats.
        Chaque élément retourné est un dict avec au moins : id_joueur, pseudo, portefeuille
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    if limit is not None:
                        cursor.execute(
                            """
                            SELECT id_joueur, pseudo, portefeuille
                            FROM joueur
                            ORDER BY portefeuille DESC
                            LIMIT %(limit)s;
                            """,
                            {"limit": limit},
                        )
                    else:
                        cursor.execute(
                            """
                            SELECT id_joueur, pseudo, portefeuille
                            FROM joueur
                            ORDER BY portefeuille DESC;
                            """
                        )
                    res = cursor.fetchall()
        except Exception as e:
            logging.exception(e)
            res = []

        return res or []

    # --------------------------------------------------------------------------

    @log
    def code_de_parrainage_existe(self, code: str) -> bool:
        """
        Vérifie si une valeur de code de parrainage existe déjà.
        Retourne True si le code existe, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT 1
                        FROM joueur
                        WHERE code_de_parrainage = %(code)s
                        LIMIT 1;
                        """,
                        {"code": code},
                    )
                    res = cursor.fetchone()
        except Exception as e:
            logging.exception(e)
            return False

        return res is not None

    # --------------------------------------------------------------------------

    @log
    def mettre_a_jour_code_de_parrainage(self, id_joueur: int, nouveau_code: str) -> bool:
        """
        Met à jour la valeur du code_de_parrainage pour un joueur donné.
        Retourne True si une ligne a été modifiée, False sinon.
        """
        try:
            with DBConnection().connection as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE joueur
                        SET code_de_parrainage = %(nouveau_code)s
                        WHERE id_joueur = %(id_joueur)s;
                        """,
                        {"nouveau_code": nouveau_code, "id_joueur": id_joueur},
                    )
                    rowcount = cursor.rowcount
        except Exception as e:
            logging.exception(e)
            return False

        return rowcount == 1
