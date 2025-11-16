from utils.log_decorator import log

from business_object.partie import Partie, EtatPartie
from business_object.joueurs import Joueur


class PartieService:
    """Service pour gérer les interactions avec une Partie via API."""

    @log
    def __init__(self, partie: Partie):
        self.partie = partie

    @log
    def voir_etat_partie(self) -> tuple[bool, str]:
        """Retourne si la requête est valide (toujours True ici)."""
        self.partie._mettre_a_jour_etat()
        return True, self.partie.etat, ""

    @log
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

    @log
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

    @log
    def se_coucher(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."

        self.partie.actions_joueur(pseudo, "se_coucher")
        return True, self.partie.etat, ""

    @log
    def all_in(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."

        self.partie.actions_joueur(pseudo, "all-in")
        return True, self.partie.etat, ""

    @log
    def rejoindre_partie(self, joueur: Joueur) -> tuple[bool, EtatPartie, str]:
        """
        Le joueur est déjà dans la table (ajouté via rejoindre_table).
        Cette fonction vérifie juste s’il peut rejoindre la main ou s’il
        doit aller en liste d’attente.
        """

        etat = self.partie.etat  # raccourci lisible

        # Vérifier le solde
        if joueur.solde < Partie.GROSSE_BLIND:
            return False, etat, (
                f"{joueur.pseudo} n'a pas assez de jetons pour jouer "
                f"(minimum {Partie.GROSSE_BLIND})."
            )

        # -------------------------
        # CAS 1 : partie terminée
        # -------------------------
        if etat.finie:
            relance = self.partie.gestion_rejouer()

            if relance:
                return True, etat, (
                    f"{joueur.pseudo} rejoint la partie. Nouvelle main lancée."
                )
            else:
                return True, etat, (
                    f"{joueur.pseudo} rejoint la table, mais la partie ne peut pas être relancée."
                )

        # -------------------------
        # CAS 2 : partie en cours
        # -------------------------

        # Déjà en liste d'attente ?
        if any(j["pseudo"] == joueur.pseudo for j in etat.liste_attente):

            return True, etat, f"{joueur.pseudo} est déjà en liste d'attente."

        # Ajouter en liste d'attente
        self.partie.ajouter_a_liste_attente(joueur)

        return True, etat, (
            f"Partie en cours : {joueur.pseudo} est ajouté à la liste d'attente "
            "et rejoindra la prochaine main."
        )

    @log
    def decision_rejouer(self, pseudo: str, veut_rejouer: bool) -> tuple[bool, EtatPartie, str]:
        if pseudo not in self.partie.etat.rejouer:
            return False, self.partie.etat, f"{pseudo} n'était pas dans la main précédente."
        
        etat = self.partie.reponse_rejouer(pseudo, veut_rejouer)
        return True, etat, f"{pseudo} {'veut rejouer' if veut_rejouer else 'quitte la table'}."