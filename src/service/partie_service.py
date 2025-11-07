class PartieService:
    """Service pour gérer les interactions avec une Partie via API."""

    def __init__(self, partie: Partie):
        self.partie = partie

    def voir_etat_partie(self) -> EtatPartie:
        """Retourne l'état actuel de la partie."""
        self.partie._mettre_a_jour_etat()
        return self.partie.etat

    def miser(self, pseudo: str, montant: int) -> EtatPartie:
        """Le joueur mise un montant."""
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur or not joueur.actif:
            return self.partie.etat  # action impossible

        if montant <= 0 or montant + joueur.mise < self.partie.mise_max:
            return self.partie.etat  # montant invalide

        return self.partie.actions_joueur(pseudo, "miser", montant)

    def suivre(self, pseudo: str) -> EtatPartie:
        """Le joueur suit la mise actuelle."""
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur or not joueur.actif:
            return self.partie.etat
        return self.partie.actions_joueur(pseudo, "suivre")

    def se_coucher(self, pseudo: str) -> EtatPartie:
        """Le joueur se couche."""
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur or not joueur.actif:
            return self.partie.etat
        return self.partie.actions_joueur(pseudo, "se_coucher")

    def all_in(self, pseudo: str) -> EtatPartie:
        """Le joueur fait all-in."""
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur or not joueur.actif:
            return self.partie.etat
        return self.partie.actions_joueur(pseudo, "all-in")

    def passer_tour(self) -> EtatPartie:
        """Passe au tour suivant (flop, turn, river)."""
        self.partie.passer_tour()
        return self.partie.etat

    def annoncer_resultats(self) -> EtatPartie:
        """Annonce les résultats de la main et met à jour l'état."""
        return self.partie.annoncer_resultats()

    def gestion_rejouer(self, reponses: dict[str, bool]) -> bool:
        """Met à jour la table selon qui veut rejouer et renvoie si la partie peut continuer."""
        return self.partie.gestion_rejouer(reponses)
