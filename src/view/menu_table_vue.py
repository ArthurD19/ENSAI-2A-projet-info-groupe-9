from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.menu_joueur_vue import MenuJoueurVue
from client.api_client import get, post, APIError


class MenuTableVue(VueAbstraite):
    """Vue du menu du joueur pendant une partie de poker via API"""

    def __init__(self, message="", id_table=None):
        super().__init__(message)
        self.id_table = id_table
        self.pseudo = Session().joueur
        self.joueur_courant = None  # sera mis à jour à chaque affichage

    def afficher_etat_partie(self):
        """Affiche l'état actuel de la partie et met à jour le joueur courant"""
        try:
            etat = get("/joueur_en_jeu/voir_etat_partie", params={"partie": self.id_table})
        except APIError as e:
            print(f"\nErreur API lors de la récupération de l'état : {e}\n")
            return None

        self.joueur_courant = etat.get("joueur_courant")

        print("\n" + "-"*50)
        print(f"Table {self.id_table} | Tour actuel : {etat['tour_actuel']}")
        print(f"Pot principal : {etat['pot']} | Mise max : {etat['mise_max']}")
        print(f"Joueur courant : {self.joueur_courant}\n")
        print("Joueurs :")
        for j in etat["joueurs"]:
            actif = "(actif)" if j["actif"] else "(couché)"
            print(f" - {j['pseudo']:10} | Solde : {j['solde']:5} | Mise : {j['mise']:5} {actif}")
        print("Board :", " ".join(etat["board"]) if etat["board"] else "vide")
        print("-"*50)
        return etat

    def voir_mes_cartes(self):
        """Affiche les cartes du joueur"""
        try:
            cartes = get("/joueur_en_jeu/voir_mes_cartes", params={"partie": self.id_table, "pseudo": self.pseudo})
            print(f"\nVos cartes : {cartes}\n")
        except APIError as e:
            print(f"\nErreur API : {e}\n")

    def choisir_menu(self):
        """Affichage du menu joueur en table"""
        self.afficher()
        etat = self.afficher_etat_partie()
        if etat is None:
            input("Appuyez sur Entrée pour continuer...")
            return self

        if self.joueur_courant != self.pseudo:
            print(f"\nCe n'est pas votre tour, veuillez patienter...\n")
            input("Appuyez sur Entrée pour rafraîchir...")
            return self

        choix = inquirer.select(
            message="Que voulez-vous faire ?",
            choices=[
                "Voir mes cartes",
                "Miser",
                "Suivre",
                "All-in",
                "Se coucher",
                "Revenir au menu joueur"
            ]
        ).execute()

        try:
            # Récupérer le solde actuel du joueur pour certaines actions
            solde_joueur = next(j['solde'] for j in etat['joueurs'] if j['pseudo'] == self.pseudo)

            if choix == "Voir mes cartes":
                self.voir_mes_cartes()

            elif choix == "Miser":
                montant = int(inquirer.text(message="Montant à miser :").execute())
                res = post(
                    "/joueur_en_jeu/miser",
                    json={
                        "pseudo": self.pseudo,
                        "portefeuille": solde_joueur,
                        "partie": self.id_table,
                        "montant": montant
                    },
                    params={"partie": self.id_table}
                )
                print(f"\n{res.get('message_retour', 'Mise effectuée')}\n")

            elif choix == "Suivre":
                res = post(
                    "/joueur_en_jeu/suivre",
                    json={
                        "pseudo": self.pseudo,
                        "portefeuille": solde_joueur,
                        "partie": self.id_table
                    },
                    params={"partie": self.id_table}
                )
                print(f"\n{res.get('message_retour', 'Action suivie')}\n")

            elif choix == "All-in":
                res = post(
                    "/joueur_en_jeu/all_in",
                    json={
                        "pseudo": self.pseudo,
                        "portefeuille": solde_joueur,
                        "partie": self.id_table
                    },
                    params={"partie": self.id_table}
                )
                print(f"\n{res.get('message_retour', 'All-in effectué')}\n")

            elif choix == "Se coucher":
                res = post(
                    "/joueur_en_jeu/se_coucher",
                    json={
                        "pseudo": self.pseudo,
                        "portefeuille": solde_joueur,
                        "partie": self.id_table
                    },
                    params={"partie": self.id_table}
                )
                print(f"\n{res.get('message_retour', 'Vous vous êtes couché')}\n")

            elif choix == "Revenir au menu joueur":
                # Quitter la table via l'API
                try:
                    message = post(
                        "/joueur_en_jeu/quitter_table",
                        params={"pseudo": self.pseudo, "id_table": self.id_table}
                    )
                    print(f"\n{message}\n")
                except APIError as e:
                    print(f"\nErreur API lors de quitter la table : {e}\n")
                return MenuJoueurVue("", None)

        except APIError as e:
            print(f"\nErreur API lors de '{choix}' : {e}\n")
        except ValueError:
            print("\nMontant invalide.\n")

        input("Appuyez sur Entrée pour continuer...")
        return self
