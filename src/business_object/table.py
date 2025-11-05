from business_object.cartes import Carte, Deck
from business_object.joueurs import Joueur

class Table:
    def __init__(self, id, blind=10):
        self.id = id
        self.joueurs = []
        self.blind = blind
        self.pot = 0
        self.indice_dealer = 0
        self.deck = Deck()
        self.board = []

    def ajouter_joueur(self, joueur: Joueur):
        if joueur in self.joueurs:
            return 2
        if len(self.joueurs) >= 5:
            return 3
            self.joueurs.append(joueur)
        self.joueurs.append(joueur)
        return 1

    def supprimer_joueur(self, joueur: Joueur):
        if joueur not in self.joueurs:
            raise ValueError("Ce joueur n'est pas à la table.")
        self.joueurs.remove(joueur)

    def reset_table(self):
        """Prépare la table pour une nouvelle main."""
        self.pot = 0
        self.board = []
        self.deck = Deck()
        self.deck.remplir()
        self.deck.melanger()

    def __repr__(self):
        return f"Table {self.id} - Joueurs: {[j.pseudo for j in self.joueurs]}"
