from dao.db_connection import DBConnection

with DBConnection().connection as conn:
    with conn.cursor() as cur:
        cur.execute("SHOW search_path;")
        print("search_path:", cur.fetchone())

        cur.execute("""
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_name IN ('players','joueurs','joueurs_statistiques','player_stats');
        """)
        print("tables trouvées:", cur.fetchall())
