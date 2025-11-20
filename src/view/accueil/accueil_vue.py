from InquirerPy import inquirer
from src.view.vue_abstraite import VueAbstraite
from src.utils.log_decorator import log


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    @log
    def __init__(self, titre: str = "", tables=None):
        self.titre = titre
        super().__init__(titre)
        self.tables = tables

    @log
    def choisir_menu(self):
        """Affiche le menu d'accueil et oriente vers la vue suivante"""

        print("\n" + "-" * 50)
        print("Accueil")
        print("-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix :",
            choices=[
                "Se connecter",
                "Créer un compte",
                "Quitter",
            ],
        ).execute()

        match choix:
            case "Quitter":
                print("\nMerci d'avoir utilisé l'application. À bientôt ! \n")
                raise SystemExit(0)

            case "Se connecter":
                from src.view.accueil.connexion_vue import ConnexionVue
                return ConnexionVue("Connexion à l'application", self.tables)

            case "Créer un compte":
                from src.view.accueil.inscription_vue import InscriptionVue
                return InscriptionVue("Création de compte joueur", self.tables)
