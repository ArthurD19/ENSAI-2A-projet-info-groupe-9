import os
import logging
import dotenv

from unittest import mock

from src.utils.log_decorator import log
from src.utils.singleton import Singleton
from src.dao.db_connection import DBConnection


class ResetDatabase(metaclass=Singleton):
    """
    Reinitialisation de la base de données
    """

    @log
    def lancer(self):
        """
        Lancement de la réinitialisation des données
        Réinitialisation des données de test si POSTGRES_SCHEMA est contient test sinon réinitialisation des 
        données globales
        """
        dotenv.load_dotenv()

        schema = os.environ["POSTGRES_SCHEMA"]

        if not schema:
            raise ValueError("POSTGRES_SCHEMA n'est pas défini dans les variables d'environnement")

        if "test" in schema.lower():
            pop_data_path = "data/pop_db_test.sql"
        else:
            pop_data_path = "data/pop_db.sql"

        try:
            with open("data/init_db.sql", encoding="utf-8") as f:
                init_db_sql = f.read()
            with open(pop_data_path, encoding="utf-8") as f:
                pop_db_sql = f.read()
        except FileNotFoundError as e:
            logging.error(f"Fichier SQL manquant : {e}")
            raise

        # Créer le schéma et initialiser la base
        create_schema_sql = f"DROP SCHEMA IF EXISTS {schema} CASCADE; CREATE SCHEMA {schema};"

        try:
            with DBConnection().connection as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_schema_sql)
                    cursor.execute(f"SET search_path TO {schema};")
                    cursor.execute(init_db_sql)
                    cursor.execute(pop_db_sql)
        except Exception as e:
            logging.error(f"Erreur lors de la réinitialisation de la base : {e}")
            raise

        logging.info(f"Schéma '{schema}' réinitialisé avec succès")
        return True