from InquirerPy import inquirer
from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.view.menu_joueur_vue import MenuJoueurVue
from src.view.menu_table_vue import MenuTableVue
from src.client.api_client import get, post, APIError
from src.utils.log_decorator import log


class MenuRejoindreTableVue(VueAbstraite):
    """Vue du menu du joueur pour rejoindre une table"""

    def __init__(self, message=""):
        super().__init__(message)
        self.pseudo = Session().joueur

    @log
    def choisir_menu(self):
        self.afficher()

        try:
            tables = get("/joueur_connecte/voir_tables")
        except APIError as e:
            print(f"\nErreur API lors de la récupération des tables : {e}\n")
            input("Appuyez sur Entrée pour revenir au menu joueur...")
            return MenuJoueurVue("", None)

        if not tables:
            print("Aucune table disponible pour le moment.")
            input("Appuyez sur Entrée pour revenir au menu joueur...")
            return MenuJoueurVue("", None)

        # Construire la liste des choix avec ID + nombre de joueurs
        choices = [f"{t['id']} (joueurs: {t['nb_joueurs']})" for t in tables]
        choices.append("Retour")

        choix = inquirer.select(
            message="Choisissez une table :",
            choices=choices
        ).execute()

        if choix == "Retour":
            return MenuJoueurVue("", None)

        # Récupérer l'ID de la table sélectionnée
        id_table = int(choix.split(" ")[0])

        try:
            # POST JSON pour rejoindre la table
            res = post("/joueur_connecte/rejoindre_table", params={"pseudo": self.pseudo, "id_table": id_table})
            if res["succes"]:
                print("")
                print(f"{res["message"]}")
                print("")
                input("Appuyez sur Entrée pour continuer...")
                return MenuTableVue(id_table=id_table)
            else:
                print("")
                print(f"{res["message"]}")
                print("")
                input("Appuyer sur Entrée pour revenir à la page d'accueil.")
                return MenuJoueurVue("", None)
        except APIError as e:
            print(f"\nErreur API : {e}\n")
            input("Appuyez sur Entrée pour revenir au menu précédent...")
            return self
