from business_object.partie import Partie
from business_object.joueurs import Joueur
from business_object.table import Table

from dao.joueur_dao import JoueurDao

from utils.singleton import Singleton
from utils.log_decorator import log

class PartieService(metaclass=Singleton):
    def __init__(self):
        self.parties = {}

    @log
    def creer_partie(self, table: Table):
        """
        Crée une partie pour une table donnée à partir des joueurs déjà présents.
        """
        if not table.joueurs or len(table.joueurs) < 2:
            raise ValueError("Il faut au moins 2 joueurs pour créer une partie")
        
        partie = Partie(id=table.id, table=table)
        self.parties[table.id] = partie
        return partie

    @log
    def rejoindre_partie(self, pseudo: str, table: Table):
        """
        Permet à un joueur web de rejoindre une table et de devenir un joueur poker.
        """
        solde = JoueurDao().valeur_portefeuille(pseudo)
        joueur = Joueur(pseudo=pseudo, solde=solde)
        
        # Ajout à la table
        ajout = table.ajouter_joueur(joueur)
        if ajout != 1:
            return ajout  # retourne le code d'erreur de table (2= déjà présent, 3= pleine)
        
        return 1

    @log
    def lancer_tour(self, id_table: int):
        """
        Lance la partie sur la table donnée.
        """
        partie = self.parties.get(id_table)
        if not partie:
            raise ValueError("Aucune partie sur cette table")
        
        partie.demarrer_partie()
        return partie

    @log
    def recuperer_partie(self, id_table: int):
        """
        Renvoie la partie en cours pour une table.
        """
        return self.parties.get(id_table)
