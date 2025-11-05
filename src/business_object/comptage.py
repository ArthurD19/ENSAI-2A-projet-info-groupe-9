from business_object.joueurs import Joueur

class Comptage:
    def __init__(self):
        self.pot = 0
        self.pots_perso = {}  

    def ajouter_pot_perso(self, joueur: Joueur, montant: int):
        self.pots_perso[joueur] = self.pots_perso.get(joueur, 0) + montant

    def ajouter_pot(self):
        """Ajoute toutes les mises perso au pot principal et reset les mises perso"""
        for montant in self.pots_perso.values():
            self.pot += montant
        self.pots_perso = {}

    def distrib_pots(self, gagnants: list[Joueur]):
        """Distribue le pot principal aux gagnants"""
        if not gagnants:
            return
        part = self.pot // len(gagnants)
        for j in gagnants:
            j.solde += part
        self.pot = 0
        self.pots_perso = {}
