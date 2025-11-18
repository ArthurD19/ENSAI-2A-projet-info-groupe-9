from src.business_object.cartes import Carte, Deck
from src.business_object.joueurs import Joueur

class Distrib:
    """Distribue les cartes pour Texas Hold'em"""

    def __init__(self, joueurs: list[Joueur])->None:
        self.joueurs = joueurs
        self.deck = Deck()
        self.deck.remplir()
        self.deck.melanger()
        self.flop = []
        self.turn = None
        self.river = None
        self.tour_actuel = "preflop"

    def distribuer_mains(self)->None:
        """distribue les mains de joueurs"""
        for j in self.joueurs:
            j.reset_main()
        for _ in range(2):
            for j in self.joueurs:
                j.recevoir_du_deck(self.deck)
        self.tour_actuel = "preflop"

    def distribuer_flop(self)->None:
        """distribue les 3 première cartes"""
        if len(self.joueurs) <= 1:
            return
        self.deck.tirer()  # brulage
        self.flop = [self.deck.tirer() for _ in range(3)]
        self.tour_actuel = "flop"

    def distribuer_turn(self)->None:
        """distribue la 4eme carte"""
        if len(self.joueurs) <= 1:
            return
        self.deck.tirer() # brulage
        self.turn = self.deck.tirer()
        self.tour_actuel = "turn"

    def distribuer_river(self)->None:
        """distribue la 4eme carte"""
        if len(self.joueurs) <= 1:
            return
        self.deck.tirer() # brulage
        self.river = self.deck.tirer()
        self.tour_actuel = "river"
