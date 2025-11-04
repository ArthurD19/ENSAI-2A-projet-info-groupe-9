from business_object.cartes import Carte, Deck
from business_object.joueurs import Joueur

class Distrib:
    """Distribue les cartes pour Texas Hold'em"""

    def __init__(self, joueurs: list[Joueur]):
        self.joueurs = joueurs
        self.deck = Deck()
        self.deck.remplir()
        self.deck.melanger()
        self.flop = []
        self.turn = None
        self.river = None
        self.tour_actuel = "preflop"

    def distribuer_mains(self):
        for j in self.joueurs:
            j.reset_main()
        for _ in range(2):
            for j in self.joueurs:
                j.recevoir_du_deck(self.deck)
        self.tour_actuel = "preflop"

    def distribuer_flop(self):
        if len(self.joueurs) <= 1:
            return
        self.deck.tirer()  # brûlée
        self.flop = [self.deck.tirer() for _ in range(3)]
        self.tour_actuel = "flop"

    def distribuer_turn(self):
        if len(self.joueurs) <= 1:
            return
        self.deck.tirer()
        self.turn = self.deck.tirer()
        self.tour_actuel = "turn"

    def distribuer_river(self):
        if len(self.joueurs) <= 1:
            return
        self.deck.tirer()
        self.river = self.deck.tirer()
        self.tour_actuel = "river"
