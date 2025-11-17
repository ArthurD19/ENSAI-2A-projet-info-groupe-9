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

    def afficher_etat_partie(self):
        """Affiche l'état actuel de la partie"""
        try:
            etat = get("/joueur_en_jeu/voir_etat_partie", params={"partie": self.id_table})
        except APIError as e:
            print(f"\nErreur API lors de la récupération de l'état : {e}\n")
            return None

        print("\n" + "-"*50)
        print(f"Table {self.id_table} | Tour actuel : {etat['tour_actuel']}")
        print(f"Pot principal : {etat['pot']} | Mise max : {etat['mise_max']}")
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
        self.afficher()
        self.afficher_etat_partie()
        print()

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

        action_map = {
            "Miser": "/joueur_en_jeu/miser",
            "Suivre": "/joueur_en_jeu/suivre",
            "All-in": "/joueur_en_jeu/all_in",
            "Se coucher": "/joueur_en_jeu/se_coucher"
        }

        if choix == "Voir mes cartes":
            self.voir_mes_cartes()
            input("Appuyez sur Entrée pour continuer...")
            return self

        elif choix in action_map:
            data = {"pseudo": self.pseudo}
            params = {"partie": self.id_table}

            if choix == "Miser":
                montant = inquirer.text(message="Montant à miser :").execute()
                try:
                    params["montant"] = int(montant)
                except ValueError:
                    print("\nMontant invalide.\n")
                    input("Appuyez sur Entrée pour continuer...")
                    return self

            try:
                res = post(action_map[choix], json=data, params=params)
                print(f"\n{res.get('message_retour', 'Action effectuée')}\n")
            except APIError as e:
                print(f"\nErreur API lors de '{choix}' : {e}\n")
            input("Appuyez sur Entrée pour continuer...")
            return self

        elif choix == "Revenir au menu joueur":
            return MenuJoueurVue("", None)
