from src.business_object.table import Table
from src.business_object.joueurs import Joueur
from src.business_object.partie import  Partie

from src.service.partie_service import PartieService

from src.utils.singleton import Singleton
from src.utils.log_decorator import log

from src.dao.joueur_dao import JoueurDao

class TableService(metaclass=Singleton):

    def __init__(self, nb_tables=10, blind=20):
        """
        Initialise les tables avec un nombre de tables et un blind par défaut
        """
        self.tables = {}
        self.parties = {}
        for i in range(1, nb_tables + 1):
            self.tables[i] = Table(id=i, blind=blind)
            self.parties[i] = Partie(id=i, table=self.tables[i])

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
        Permet à un joueur de rejoindre une table si elle existe et qu'il y reste de la place.
        Ajoute automatiquement le joueur à la partie associée à la table.

        Parameters
        ----------
        pseudo: str
            Pseudo du joueur qui veut rejoindre
        id_table: int
            Identifiant de la table que le joueur veut rejoindre

        Returns
        -------
        tuple[bool, EtatPartie, str]
            bool: True si le joueur a pu rejoindre (ou a été mis en attente)
            EtatPartie: état actuel de la partie
            str: message d'information
        """
        # Récupérer le solde depuis la DAO
        solde = JoueurDao().valeur_portefeuille(pseudo)
        if solde == None:
            solde = 1000
        joueur = Joueur(pseudo, solde)
        # Récupérer la table
        table = self.get_table(id_table)

        if not table:
            return False, None, f"La table {id_table} n'existe pas."
        print("good")
        
        if any(j.pseudo == pseudo for j in table.joueurs):
            partie = self.parties.get(id_table)
            return False, partie.etat, f"{pseudo} est déjà à la table {id_table}."

        # Ajouter le joueur à la table
        code_table = table.ajouter_joueur(joueur)  # 1=ok, 2=table pleine, etc.
        if code_table != 1:
            return False, None, "Impossible de rejoindre la table (pleine ou erreur)."

        # Ajouter le joueur à la partie associée
        partie = self.parties.get(id_table)
        partie.table = table

        if partie is None:
            return True, None, f"{pseudo} ajouté à la table {id_table}, mais aucune partie n'est définie."

        # Appeler rejoindre_partie sur la partie
        partie_service = PartieService(partie)
        success, etat, msg = partie_service.rejoindre_partie(joueur)
        partie = partie_service.partie
        self.parties[id_table] = partie
        return success, etat, msg


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
    def quitter_table(self, pseudo: str, id_table: int):
        """
        Supprime un joueur de la table et de la partie associée.
        """
        table = self.tables.get(id_table)
        if not table:
            return 2  # Table non trouvée

        # Supprimer le joueur de la table
        for j in table.joueurs:
            if j.pseudo == pseudo:
                table.supprimer_joueur(j)
                break

        # Mettre à jour la partie associée
        partie = self.parties.get(id_table)
        if partie:
            # Supprimer le joueur de la liste des joueurs de la partie
            partie.table.joueurs = [j for j in partie.table.joueurs if j.pseudo != pseudo]
            # Mettre à jour l'état de la partie
            partie._mettre_a_jour_etat()

        return 1  # Succès


    @log
    def reset_table(self, id_table):
        table = self.tables[id_table]
        table.reset_table()
        self.tables[id_table] = table
    
    @log
    def etat_tables(self):
        """
        Renvoie la liste de toutes les tables avec les joueurs présents.
        
        Returns
        -------
        List[dict]: une liste où chaque élément contient :
            - id : identifiant de la table
            - blind : blind de la table
            - joueurs : liste des pseudos des joueurs
        """
        etat = []

        for id_table, table in self.tables.items():
            etat.append({
                "table": id_table,
                "blind": table.blind,
                "joueurs": [j.pseudo for j in table.joueurs]
            })

        return etat