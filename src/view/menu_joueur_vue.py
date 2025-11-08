from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session
from client.api_client import get, post, APIError
from service.joueur_service import JoueurService

class MenuJoueurVue(VueAbstraite):
    """Vue du menu du joueur via API"""

    def __init__(self, titre, tables):
        super().__init__(titre)
        self.tables = tables

    def choisir_menu(self):
        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Rejoindre une table",
                "Afficher la valeur du portefeuille",
                "Afficher le classement",
                "Afficher les statistiques", 
                "Générer ou voir mon code de parrainage",
                "Se déconnecter",
            ],
        ).execute()

        pseudo = Session().joueur

        match choix:

            case "Se déconnecter":
                pseudo = Session().joueur
                success = JoueurService().se_deconnecter(pseudo)
                from view.accueil.accueil_vue import AccueilVue
                message = "Vous êtes maintenant déconnecté." if success else "Erreur lors de la déconnexion."
                return AccueilVue(message, self.tables)


            case "Afficher la valeur du portefeuille":
                try:
                    portefeuille = get("/joueur_connecte/valeur_portefeuille", params={"pseudo": pseudo})
                    print(f"\nVotre portefeuille contient : {portefeuille} jetons.\n")
                except APIError as e:
                    print(f"Erreur API : {e}")
                input("Appuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue("", self.tables)

            case "Afficher le classement":
                try:
                    classement_joueur = get("/joueur_connecte/voir_classement")
                    print("\nClassement des joueurs :")
                    print("-" * 40)
                    max_pseudo_len = max(len(j["pseudo"]) for j in classement_joueur)
                    max_credit_len = max(len(str(j["portefeuille"])) for j in classement_joueur)
                    for i, joueur in enumerate(classement_joueur, start=1):
                        pseudo_joueur = joueur["pseudo"]
                        portefeuille = joueur["portefeuille"]
                        if pseudo_joueur == pseudo:
                            print(f">>> {i:>2}. {pseudo_joueur:<{max_pseudo_len}}   {portefeuille:>{max_credit_len}} crédits (vous)")
                        else:
                            print(f"    {i:>2}. {pseudo_joueur:<{max_pseudo_len}}   {portefeuille:>{max_credit_len}} crédits")
                    print("-" * 40)
                except APIError as e:
                    print(f"Erreur API : {e}")
                input("\nAppuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue("", self.tables)

            case "Afficher les statistiques":
                try:
                    stats = get("/joueur_connecte/stats", params={"pseudo": pseudo})
                    print("\nVos statistiques :")
                    print("-" * 50)
                    for champ, valeur in stats.items():
                        print(f"{champ:<30} : {valeur}")
                    print("-" * 50)
                except APIError as e:
                    print(f"Erreur API : {e}")
                input("\nAppuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue("", self.tables)

            case "Générer ou voir mon code de parrainage":
                try:
                    code_parrainage = get("/joueur_connecte/code_parrainage", params={"pseudo": pseudo})
                    print(f"\nVotre code de parrainage est : {code_parrainage}\n")
                except APIError as e:
                    print(f"Erreur API : {e}")
                input("Appuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue("", self.tables)

            case "Rejoindre une table":
                from view.menu_rejoindre_table_vue import MenuRejoindreTableVue
                return MenuRejoindreTableVue(self.tables)
