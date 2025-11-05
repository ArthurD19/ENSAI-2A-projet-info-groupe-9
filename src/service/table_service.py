from business_object.table import Table
from business_object.joueurs import Joueur

from utils.singleton import Singleton
from utils.log_decorator import log

from dao.joueur_dao import JoueurDao

class TableService(metaclass=Singleton):
    @log
    def get_table(self, id_table: int):
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

    @log
    def rejoindre_table(self, pseudo: str, id_table: int):
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
        solde = JoueurDao().valeur_portefeuille(pseudo)
        joueur_partie = Joueur(pseudo, solde)
        table = self.get_table(id_table)
        if not table:
            return 4
        return table.ajouter_joueur(joueur_partie)

    @log
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
                "blind": t.blind
            }
            for t in self.tables.values()
        ]

    @log
    def quitter_table(self, pseudo, id_table):
        """
        Supprime un joueur de la table demandée à partir de son pseudo
        
        Parameters
        ----------
        pseudo: str
            pseudo du joueur que l'on veut supprimer
        id_table: int
            identifiant de la table où l'on veut supprimer le joueur
            
        Returns
        -------
        int: 1 si le joueur est supprimé et 2 sinon"""
        table = self.tables[id_table]
        joueurs = table.joueurs
        for j in joueurs:
            if j.pseudo == pseudo:
                table.supprimer_joueur(j)
                self.tables[id_table] = table
                return 1
        return 2

    @log
    def reset_table(self, id_table):
        table = self.tables[id_table]
        table.reset_table()
        self.tables[id_table] = table