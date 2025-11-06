from business_object.cartes import Carte, Deck

class Joueur:
    def __init__(self, pseudo: str, solde: int)->None:
        self.pseudo = pseudo
        self.solde = solde
        self.main = []
        self.mise = 0
        self.actif = True

    def recevoir_carte(self, carte: Carte)->None:
        if len(self.main) >= 2:  
            raise ValueError("Le joueur a déjà 2 cartes.")
        self.main.append(carte)

    def recevoir_du_deck(self, deck: Deck)->None:
        """Pioche une carte depuis le deck et l'ajoute à la main."""
        carte = deck.tirer()
        self.recevoir_carte(carte)

    def reset_main(self)->None:
        self.main = []
        self.mise = 0
        self.actif = True

    def miser(self, montant: int)->int:
        if montant > self.solde:
            raise ValueError("Solde insuffisant.")
        self.solde -= montant
        self.mise += montant
        return montant

    def suivre(self, montant: int)->int:
        to_pay = montant - self.mise
        return self.miser(to_pay)

    def se_coucher(self)->None:
        self.actif = False

    def __repr__(self)->str:
        return f"{self.pseudo} ({self.solde} jetons, main={self.main})"
