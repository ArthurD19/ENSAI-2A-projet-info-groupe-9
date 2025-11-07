class PartieService:
    """Service pour gérer les interactions avec une Partie via API."""

    def __init__(self, partie: Partie):
        self.partie = partie

    def voir_etat_partie(self) -> tuple[bool, str]:
        """Retourne si la requête est valide (toujours True ici)."""
        self.partie._mettre_a_jour_etat()
        return True, ""

    def miser(self, pseudo: str, montant: int) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, f"Le joueur '{pseudo}' n'est pas actif."
        if montant <= 0:
            return False, "Le montant doit être positif."
        if montant + joueur.mise < self.partie.mise_max:
            return False, f"Le montant doit au moins égaler la mise maximale ({self.partie.mise_max})."
        if montant > joueur.solde:
            return False, f"Montant {montant} supérieur au solde de {joueur.solde}, tu peux all-in"

        self.partie.actions_joueur(pseudo, "miser", montant)
        return True, ""

    def suivre(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, f"Le joueur '{pseudo}' n'est pas actif."
        if self.partie.mise_max > joueur.solde:
            return False, f"Montant {montant} supérieur au solde de {joueur.solde}, tu peux all-in"

        self.partie.actions_joueur(pseudo, "suivre")
        return True, ""

    def se_coucher(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, f"Le joueur '{pseudo}' n'est pas actif."

        self.partie.actions_joueur(pseudo, "se_coucher")
        return True, ""

    def all_in(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, f"Le joueur '{pseudo}' n'est pas actif."

        self.partie.actions_joueur(pseudo, "all-in")
        return True, ""

    def rejoindre_partie(self, joueur: Joueur) -> tuple[bool, str]:
        """
        Permet à un nouveau joueur de rejoindre la table.
        Pas besoin de vérifier son solde.
        Si la partie peut repartir, elle se relance automatiquement.
        """
        # Vérifier que le joueur n'est pas déjà à la table
        if any(j.pseudo == joueur.pseudo for j in self.partie.table.joueurs):
            return False, f"Le joueur '{joueur.pseudo}' est déjà à la table."

        # Ajouter le joueur
        self.partie.table.ajouter_joueur(joueur)

        # Appeler gestion_rejouer pour réinitialiser l'état et éventuellement relancer la partie
        partie_relancee = self.partie.gestion_rejouer()

        if partie_relancee:
            return True, "Nouvelle main lancée."
        else:
            return False, "Pas encore assez de joueurs pour relancer la partie."

