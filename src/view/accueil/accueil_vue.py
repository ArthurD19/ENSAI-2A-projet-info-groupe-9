# src/view/accueil/accueil_vue.py
from InquirerPy import inquirer
from view.vue_abstraite import VueAbstraite
from view.session import Session


class AccueilVue(VueAbstraite):
    """Vue d'accueil de l'application"""

    def __init__(self, titre: str = "", tables=None):
        # On met explicitement l'attribut titre ici pour éviter les erreurs
        # si VueAbstraite n'initialise pas self.titre ou si on instancie AccueilVue
        # sans appeler super correctement ailleurs. Ca m'a dit de faire ca mais cest bizarre non ?
        self.titre = titre
        super().__init__(titre)
        self.tables = tables

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
                from view.accueil.connexion_vue import ConnexionVue
                return ConnexionVue("Connexion à l'application", self.tables)

            case "Créer un compte":
                from view.accueil.inscription_vue import InscriptionVue
                return InscriptionVue("Création de compte joueur", self.tables)
