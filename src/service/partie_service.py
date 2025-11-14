from business_object.partie import Partie, EtatPartie
from business_object.joueurs import Joueur


class PartieService:
    """Service pour gérer les interactions avec une Partie via API."""

    def __init__(self, partie: Partie):
        self.partie = partie

    def voir_etat_partie(self) -> tuple[bool, str]:
        """Retourne si la requête est valide (toujours True ici)."""
        self.partie._mettre_a_jour_etat()
        return True, self.partie.etat, ""

    def miser(self, pseudo: str, montant: int) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."
        if montant <= 0:
            return False, self.partie.etat, "Le montant doit être positif."
        if montant + joueur.mise < self.partie.mise_max:
            return False, self.partie.etat, f"Le montant doit au moins égaler la mise maximale ({self.partie.mise_max})."
        if montant > joueur.solde:
            return False, self.partie.etat, f"Montant {montant} supérieur au solde de {joueur.solde}, tu peux all-in"

        self.partie.actions_joueur(pseudo, "miser", montant)
        return True, self.partie.etat, ""

    def suivre(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."
        if self.partie.mise_max > joueur.solde:
            return False, self.partie.etat, f"Montant {self.mise_max} supérieur au solde de {joueur.solde}, tu peux all-in"

        self.partie.actions_joueur(pseudo, "suivre")
        return True, self.partie.etat, ""

    def se_coucher(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."

        self.partie.actions_joueur(pseudo, "se_coucher")
        return True, self.partie.etat, ""

    def all_in(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."

        self.partie.actions_joueur(pseudo, "all-in")
        return True, self.partie.etat, ""

    def rejoindre_partie(self, joueur: Joueur) -> tuple[bool, str]:
        """
        Permet à un joueur de rejoindre la partie.
        Vérifie :
        - qu'il n'est pas déjà dans la table ou la liste d'attente
        - que son solde est >= grosse blind
        - que le nombre total joueurs + liste d'attente <= 5
        Intègre les joueurs en liste d'attente automatiquement lors de gestion_rejouer.
        """
        # Vérifier le solde
        if joueur.solde < Partie.GROSSE_BLIND:
            return False, self.partie.etat, f"{joueur.pseudo} n'a pas assez de jetons pour jouer (minimum {Partie.GROSSE_BLIND})."

        # Vérifier qu'il n'est pas déjà dans la table ou la liste d'attente
        deja_present = any(j.pseudo == joueur.pseudo for j in self.partie.table.joueurs)
        #deja_en_attente = any(j.pseudo == joueur.pseudo for j in self.partie.etat.liste_attente)  
        #print("Joueurs dans table :", [j.pseudo for j in self.partie.table.joueurs])
        #print("Joueurs en liste d'attente :", [j.pseudo for j in self.partie.etat.liste_attente])
        #if deja_present or deja_en_attente:
        #    return False, self.partie.etat, f"{joueur.pseudo} est déjà dans la table ou en liste d'attente."

        # Vérifier la limite totale (table + liste d'attente <= 5)
        total_joueurs = len(self.partie.table.joueurs) + len(self.partie.etat.liste_attente)
        if total_joueurs >= 5:
            return False, self.partie.etat, "La table et la liste d'attente sont pleines."

        """
        # Ajouter le joueur à la liste d'attente
        self.partie.ajouter_a_liste_attente(joueur)
        partie_relancee = False
        if self.partie.etat.finie:
            partie_relancee = self.partie.gestion_rejouer()

        if partie_relancee:
            return True, self.partie.etat, f"{joueur.pseudo} ajouté à la liste d'attente. Nouvelle main lancée."
        else:
            return True, self.partie.etat, f"{joueur.pseudo} ajouté à la liste d'attente. Pas encore assez de joueurs pour relancer la partie."
        """
        return True, self.partie.etat, f"{joueur.pseudo} ajouté à la liste d'attente. Nouvelle main lancée."

    def decision_rejouer(self, pseudo: str, veut_rejouer: bool) -> tuple[bool, EtatPartie, str]:
        if pseudo not in self.partie.etat.rejouer:
            return False, self.partie.etat, f"{pseudo} n'était pas dans la main précédente."
        
        etat = self.partie.reponse_rejouer(pseudo, veut_rejouer)
        return True, etat, f"{pseudo} {'veut rejouer' if veut_rejouer else 'quitte la table'}."