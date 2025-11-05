from business_object.table import Table

class TableService:
    def __init__(self, nb_tables=10, blind=10):
        self.tables = {}
        for i in range(1, nb_tables + 1):
            self.tables[i] = Table(id=i, blind=blind)

    def get_table(self, id_table):
        """
        Fonction qui renvoie la table correspondant à l'identifiant si elle existe, None sinon.
        
        Parameters
        ----------
        id_table: int
            Identifiant de la table que l'on veut récupérer.
            
        Returns
        -------
        Table ou None
        """
        return self.tables.get(id_table)

    def rejoindre_table(self, joueur, id_table):
        """
        Permet à un joueur de rejoindre une table si elle existe et qu'il y reste de la place

        Parameters
        ----------
        joueur: Joueur
            Joueur (business_object qui veut rejoindre une table
        id_table: int
            Identifiant de la table que le joueur veut rejoindre

        Returns
        -------
        int 
            1 pour 
            2 pour 
            3 pour
            4 pour la table n'existe pas
        """
        table = self.get_table(id_table)
        if not table:
            return 4
        return table.ajouter_joueur(joueur)

    def lister_tables(self):
        """
        Renvoie la liste de toutes les tables
        
        Returns
        -------
        List[dict]: liste de dictionnaire où chaque élément de la liste est un dictionnaire correspondant à la table"""
        return [
            {
                "id": t.id,
                "nb_joueurs": len(t.joueurs),
                "blind": t.blind,
                "en_cours": t.en_cours
            }
            for t in self.tables.values()
        ]
