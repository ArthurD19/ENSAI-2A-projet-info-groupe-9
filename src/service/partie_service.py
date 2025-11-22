from src.utils.log_decorator import log

from src.business_object.partie import Partie, EtatPartie
from src.business_object.joueurs import Joueur


class PartieService:
    """Service pour gérer les interactions avec une Partie via API."""

    @log
    def __init__(self, partie: Partie):
        self.partie = partie

    # -----------------------------------------------------
    #  Voir l'état
    # -----------------------------------------------------
    @log
    def voir_etat_partie(self) -> tuple[bool, str]:
        self.partie._mettre_a_jour_etat()
        return True, self.partie.etat, ""

    # -----------------------------------------------------
    #  MISER
    # -----------------------------------------------------
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
            return False, self.partie.etat, (
                f"Le montant total doit atteindre la mise maximale ({self.partie.mise_max})."
            )
        if montant > joueur.solde:
            return False, self.partie.etat, (
                f"Montant {montant} supérieur au solde ({joueur.solde}), tu peux all-in."
            )
        if montant + joueur.mise < (2*self.partie.GROSSE_BLIND) and montant + joueur.mise != self.partie.GROSSE_BLIND:
            return False, self.partie.etat, (
                f"Tu peux miser la grosse blinde, deux fois celle-ci ou plus"
            )

        limite_max = self.partie.mise_max_autorisee()
        if montant + joueur.mise > limite_max:
            return False, self.partie.etat, (
                f"Tu ne peux pas miser plus que {limite_max}, "
                "car un joueur ne peut pas suivre davantage."
            )

        # Action
        self.partie.actions_joueur(pseudo, "miser", montant)

        # Tour suivant
        self.partie._mettre_a_jour_etat()

        return True, self.partie.etat, ""

    # -----------------------------------------------------
    #  SUIVRE
    # -----------------------------------------------------
    @log
    def suivre(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)

        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."

        montant_a_payer = self.partie.mise_max - joueur.mise

        if montant_a_payer > joueur.solde:
            return False, self.partie.etat, (
                f"La mise max ({self.partie.mise_max}) dépasse ton solde ({joueur.solde}), tu peux all-in."
            )

        # Action
        self.partie.actions_joueur(pseudo, "suivre")

        # Tour suivant
        self.partie._mettre_a_jour_etat()

        return True, self.partie.etat, ""

    # -----------------------------------------------------
    # SE COUCHER
    # -----------------------------------------------------
    @log
    def se_coucher(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)

        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."

        # Action
        self.partie.actions_joueur(pseudo, "se_coucher")

        # Tour suivant
        self.partie._mettre_a_jour_etat()

        return True, self.partie.etat, ""

    # -----------------------------------------------------
    #  ALL-IN
    # -----------------------------------------------------
    @log
    def all_in(self, pseudo: str) -> tuple[bool, str]:
        joueur = next((j for j in self.partie.table.joueurs if j.pseudo == pseudo), None)

        if not joueur:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'existe pas."
        if not joueur.actif:
            return False, self.partie.etat, f"Le joueur '{pseudo}' n'est pas actif."
        limite_max = self.partie.mise_max_autorisee()
        if joueur.solde + joueur.mise > limite_max:
            return False, self.partie.etat, (
                f"Tu ne peux pas all-in car tu as plus que {limite_max}, "
                f"à la place tu peux miser {limite_max-joueur.mise}."
            )
        # Action
        self.partie.actions_joueur(pseudo, "all-in")

        # Tour suivant
        self.partie._mettre_a_jour_etat()

        # S'assurer que resultats est une liste valide
        if self.partie.etat.resultats is None:
            self.partie.etat.resultats = []

        return True, self.partie.etat, ""

    # -----------------------------------------------------
    #  REJOINDRE LA PARTIE
    # -----------------------------------------------------
    @log
    def rejoindre_partie(self, joueur: Joueur) -> tuple[bool, EtatPartie, str]:

        etat = self.partie.etat

        if joueur.solde < Partie.GROSSE_BLIND:
            return False, etat, (
                f"{joueur.pseudo} n'a pas assez de jetons "
                f"(minimum {Partie.GROSSE_BLIND})."
            )

        # Partie terminée
        if etat.finie:
            relance = self.partie.gestion_rejouer()
            if relance:
                return True, etat, (
                    f"{joueur.pseudo} rejoint la partie. Nouvelle main lancée."
                )
            else:
                return True, etat, (
                    f"{joueur.pseudo} rejoint la table, mais la main ne peut pas redémarrer."
                )

        # Partie en cours → liste d'attente
        if any(j["pseudo"] == joueur.pseudo for j in etat.liste_attente):
            return True, etat, f"{joueur.pseudo} est déjà en liste d'attente."

        self.partie.ajouter_a_liste_attente(joueur)

        return True, etat, (
            f"Partie en cours : {joueur.pseudo} rejoint la liste d'attente. "
            "Merci d'attendre que vos collègues de jeu aient terminé leur main."
        )

    # -----------------------------------------------------
    # REPLAY
    # -----------------------------------------------------
    @log
    def decision_rejouer(self, pseudo: str, veut_rejouer: bool) -> tuple[bool, EtatPartie, str]:
        if pseudo not in self.partie.etat.rejouer:
            return False, self.partie.etat, (
                f"{pseudo} n'était pas dans la main précédente."
            )

        etat = self.partie.reponse_rejouer(pseudo, veut_rejouer)

        return True, etat, (
            f"{pseudo} {'veut rejouer' if veut_rejouer else 'quitte la table'}."
        )
