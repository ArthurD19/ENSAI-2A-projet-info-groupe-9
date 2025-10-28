from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.menu_joueur_vue import MenuJoueurVue
from view.menu_table_vue import MenuTableVue

from service.joueur_service import JoueurService


class MenuRejoindreTableVue(VueAbstraite):
    """Vue du menu du joueur pour rejoindre une table

    Attributes
    ----------
    message=''
        str

    Returns
    ------
    view
        retourne la prochaine vue, celle qui est choisie par l'utilisateur
    """

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur = choix de la table par le joueur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix de table : ",
            choices=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "Retour"
            ],
        ).execute()

        match choix:
            case "1":
                table = JoueurService().rejoindre_table("1")
                if table:
                    message = "Vous avez rejoint la table 1"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "2":
                table = JoueurService().rejoindre_table("2")
                if table:
                    message = "Vous avez rejoint la table 2"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)
            
            case "3":
                table = JoueurService().rejoindre_table("3")
                if table:
                    message = "Vous avez rejoint la table 3"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "4":
                table = JoueurService().rejoindre_table("4")
                if table:
                    message = "Vous avez rejoint la table 4"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "5":
                table = JoueurService().rejoindre_table("5")
                if table:
                    message = "Vous avez rejoint la table 5"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "6":
                table = JoueurService().rejoindre_table("6")
                if table:
                    message = "Vous avez rejoint la table 6"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "7":
                table = JoueurService().rejoindre_table("7")
                if table:
                    message = "Vous avez rejoint la table 7"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "8":
                table = JoueurService().rejoindre_table("8")
                if table:
                    message = "Vous avez rejoint la table 8"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "9":
                table = JoueurService().rejoindre_table("9")
                if table:
                    message = "Vous avez rejoint la table 9"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "10":
                table = JoueurService().rejoindre_table("10")
                if table:
                    message = "Vous avez rejoint la table 10"
                    return MenuTableVue(message)
                message = "Erreur : impossible de rejoindre cette table"
                return MenuRejoindreTableVue(message)

            case "Retour":
                return MenuJoueurVue()