from InquirerPy import inquirer
from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.view.menu_joueur_vue import MenuJoueurVue
from src.client.api_client import get, post, APIError
from src.business_object.partie import Partie
from src.utils.log_decorator import log


class MenuTableVue(VueAbstraite):
    """Vue du menu du joueur pendant une partie de poker via API"""

    @log
    def __init__(self, message="", id_table=None):
        super().__init__(message)
        self.id_table = id_table
        self.pseudo = Session().joueur
        self.joueur_courant = None  # sera mis à jour à chaque affichage
        self.resultats_deja_affiche = False

    @log
    def afficher_etat_partie(self):
        """Affiche l'état actuel de la partie et met à jour le joueur courant"""
        try:
            etat = get("/joueur_en_jeu/voir_etat_partie", params={"partie": self.id_table})
        except APIError as e:
            print(f"\nErreur API lors de la récupération de l'état : {e}\n")
            return None

        self.joueur_courant = etat.get("joueur_courant")
        if self.joueur_courant is not None:
            print("\n" + "-" * 50)
            print(f"Table {self.id_table} | Tour actuel : {etat['tour_actuel']}")
            print(f"Pot principal : {etat['pot']} | Mise max : {etat['mise_max']}")
            print(f"Joueur courant : {self.joueur_courant}\n")
            for j in etat["joueurs"]:
                actif = "(actif)" if j["actif"] else "(couché)"
                print(f" - {j['pseudo']:10} | Solde : {j['solde']:5} | Mise : {j['mise']:5} {actif}")

            # --- SÉPARATEUR DU BOARD ---
            print("-" * 50)

            # Board
            print("Board :", " | ".join(etat["board"]) if etat["board"] else "vide")

            print("-" * 50)
        return etat

    @log
    def voir_mes_cartes(self):
        """Affiche les cartes du joueur"""
        try:
            cartes = get("/joueur_en_jeu/voir_mes_cartes", params={"partie": self.id_table, "pseudo": self.pseudo})
            print(f"\nVos cartes : {cartes}\n")
        except APIError as e:
            print(f"\nErreur API : {e}\n")

    @log
    def choisir_menu(self):
        """Affichage du menu joueur en table"""
        self.afficher()
        etat = self.afficher_etat_partie()
        if not etat.get("finie", False):
            self.resultats_affiches = False
        if self.joueur_courant is None and etat.get("resultats") == []:
            print("Attente des autres joueurs pour relancer la partie ...")

            choix = inquirer.select(
                message="Que voulez-vous faire ?",
                choices=[
                    "Quitter la table",
                    "Continuer à attendre"
                ]).execute()
            try:
                if choix == "Quitter la table":
                    try:
                        post(
                            "/joueur_en_jeu/quitter_table",
                            params={"pseudo": self.pseudo, "id_table": self.id_table}
                            )
                        print("Vous avez été retiré de la table.")
                    except APIError as e:
                        print(f"Erreur lors de la suppression de la table : {e}")
                    return MenuJoueurVue("", None)
                elif choix == "Continuer à attendre":
                    input("Appuyez sur Entrée pour rafraîchir...")
                    return self
            except APIError as e:
                print(f"\nErreur API lors de '{choix}' : {e}\n")

        if etat.get("finie", False) and not self.resultats_deja_affiche:
            self.resultats_deja_affiche = True
            resultats = etat.get("resultats")
            gagnant = resultats[0]
            print("\nLa main est terminée !\n")
            print("\n Résultats :\n")
            print(f"\n Gagnant : {gagnant["pseudo"]}\n")
            print(f"\n Main : {gagnant["main"]}\n")
            print(f"\n {gagnant["description"]}\n")

            solde = next((j['solde'] for j in etat['joueurs'] if j['pseudo'] == self.pseudo), 0)
            peut_rejouer = solde >= Partie.GROSSE_BLIND  # 20 jetons minimum

            if self.pseudo in etat.get("rejouer", {}):
                if etat["rejouer"][self.pseudo] is None and peut_rejouer:
                    veut_rejouer = inquirer.confirm(
                        message="Voulez-vous rejouer la prochaine main ?"
                    ).execute()
                    try:
                        res = post(
                            "/joueur_en_jeu/decision_rejouer",
                            params={
                                "pseudo": self.pseudo,
                                "partie": self.id_table,
                                "veut_rejouer": veut_rejouer
                            }
                        )
                        etat["rejouer"][self.pseudo] = veut_rejouer
                        print(f"\n{res.get('message_retour', 'Réponse enregistrée')}\n")
                    except APIError as e:
                        print(f"\nErreur API : {e}\n")
                else:
                    reponse = "Oui" if etat["rejouer"].get(self.pseudo, False) else "Non"
                    print(f"Vous avez déjà répondu : {reponse}")

                    if not peut_rejouer:
                        print("Vous n'avez pas assez de jetons pour rejouer.")
                        # Supprimer le joueur de la table
                        try:
                            post(
                                "/joueur_en_jeu/quitter_table",
                                params={"pseudo": self.pseudo, "id_table": self.id_table}
                            )
                            print("Vous avez été retiré de la table.")
                        except APIError as e:
                            print(f"Erreur lors de la suppression de la table : {e}")
                        return MenuJoueurVue("", None)
                    elif reponse == "Non":
                        try:
                            post(
                                "/joueur_en_jeu/quitter_table",
                                params={"pseudo": self.pseudo, "id_table": self.id_table}
                            )
                            print("Vous avez été retiré de la table.")
                        except APIError as e:
                            print(f"Erreur lors de la suppression de la table : {e}")
                        return MenuJoueurVue("", None)
                    else:
                        print("Attente des autres joueurs pour relancer la partie...")
                        input("Appuyez sur Entrée pour rafraîchir...")
                        choix = inquirer.select(
                            message="Que voulez-vous faire ?",
                            choices=[
                                "Quitter la table",
                                "Continuer à attendre"
                            ]).execute()
                        try:
                            if choix == "Quitter la table":
                                try:
                                    post(
                                        "/joueur_en_jeu/quitter_table",
                                        params={"pseudo": self.pseudo, "id_table": self.id_table}
                                        )
                                    print("Vous avez été retiré de la table.")
                                except APIError as e:
                                    print(f"Erreur lors de la suppression de la table : {e}")
                                return MenuJoueurVue("", None)
                            elif choix == "Continuer à attendre":
                                input("Appuyez sur Entrée pour rafraîchir...")
                                return self
                        except APIError as e:
                            print(f"\nErreur API lors de '{choix}' : {e}\n")
            else:
                print("Attente des autres joueurs pour relancer la partie...")
                input("Appuyez sur Entrée pour rafraîchir...")
            return self

        if self.resultats_deja_affiche:
            solde = next((j['solde'] for j in etat['joueurs'] if j['pseudo'] == self.pseudo), 0)
            peut_rejouer = solde >= Partie.GROSSE_BLIND
            reponse = "Oui" if etat["rejouer"].get(self.pseudo, False) else "Non"
            print(f"Vous avez déjà répondu : {reponse}")

            if not peut_rejouer:
                print("Vous n'avez pas assez de jetons pour rejouer.")
                # Supprimer le joueur de la table
                try:
                    post(
                        "/joueur_en_jeu/quitter_table",
                        params={"pseudo": self.pseudo, "id_table": self.id_table}
                    )
                    print("Vous avez été retiré de la table.")
                except APIError as e:
                    print(f"Erreur lors de la suppression de la table : {e}")
                    return MenuJoueurVue("", None)
            elif reponse == "Non":
                try:
                    post(
                        "/joueur_en_jeu/quitter_table",
                        params={"pseudo": self.pseudo, "id_table": self.id_table}
                    )
                    print("Vous avez été retiré de la table.")
                except APIError as e:
                    print(f"Erreur lors de la suppression de la table : {e}")
                return MenuJoueurVue("", None)
            else:
                print("Attente des autres joueurs pour relancer la partie...")
                input("Appuyez sur Entrée pour rafraîchir...")
                choix = inquirer.select(
                    message="Que voulez-vous faire ?",
                    choices=[
                        "Quitter la table",
                        "Continuer à attendre"
                    ]).execute()
                try:
                    if choix == "Quitter la table":
                        try:
                            post(
                                "/joueur_en_jeu/quitter_table",
                                params={"pseudo": self.pseudo, "id_table": self.id_table}
                            )
                            print("Vous avez été retiré de la table.")
                        except APIError as e:
                            print(f"Erreur lors de la suppression de la table : {e}")
                        return MenuJoueurVue("", None)
                    elif choix == "Continuer à attendre":
                        input("Appuyez sur Entrée pour rafraîchir...")
                        return self
                except APIError as e:
                    print(f"\nErreur API lors de '{choix}' : {e}\n")

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
                    params={"partie": self.id_table, "montant": montant}
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
