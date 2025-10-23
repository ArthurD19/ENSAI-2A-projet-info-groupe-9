from business_object.cartes import Carte, Deck
from business_object.joueurs import Joueur


class Distrib:
    """
    Gère la distribution des cartes dans une partie de Poker Texas Hold'em.
    - Entre 2 et 5 joueurs.
    - 2 cartes privées par joueur.
    - 5 cartes communes (flop, turn, river).
    """

    def __init__(self, joueurs: list[Joueur]):
        if not 2 <= len(joueurs) <= 5:
            raise ValueError("Le nombre de joueurs doit être compris entre 2 et 5.")
        self.joueurs = joueurs
        self.deck = Deck()
        self.deck.remplir()
        self.deck.melanger()
        self.flop = []
        self.turn = None
        self.river = None
        self.tour_actuel = "preflop"  # pour suivre la progression du jeu

    # === UTILITAIRES ===
    def joueurs_actifs(self):
        """Retourne la liste des joueurs encore dans le coup."""
        return [j for j in self.joueurs if j.actif]

    def partie_terminee(self):
        """Retourne True si un seul joueur actif reste."""
        return len(self.joueurs_actifs()) <= 1

    # === DISTRIBUTION AUX JOUEURS ===
    def distribuer_mains(self):
        """Distribue deux cartes à chaque joueur."""
        for joueur in self.joueurs:
            joueur.reset_main()

        for _ in range(2):
            for joueur in self.joueurs:
                joueur.recevoir_du_deck(self.deck)
        self.tour_actuel = "preflop"

    # === DISTRIBUTION SUR LA TABLE ===
    def distribuer_flop(self):
        """Brûle une carte puis tire 3 cartes pour le flop, si la partie continue."""
        if self.partie_terminee():
            print("Tous les autres joueurs se sont couchés. Fin de la main.")
            return
        self.deck.tirer()  # carte brûlée
        self.flop = [self.deck.tirer() for _ in range(3)]
        self.tour_actuel = "flop"

    def distribuer_turn(self):
        """Brûle une carte puis tire le turn, si la partie continue."""
        if self.partie_terminee():
            print("Tous les autres joueurs se sont couchés. Fin de la main.")
            return
        self.deck.tirer()
        self.turn = self.deck.tirer()
        self.tour_actuel = "turn"

    def distribuer_river(self):
        """Brûle une carte puis tire la river, si la partie continue."""
        if self.partie_terminee():
            print("Tous les autres joueurs se sont couchés. Fin de la main.")
            return
        self.deck.tirer()
        self.river = self.deck.tirer()
        self.tour_actuel = "river"