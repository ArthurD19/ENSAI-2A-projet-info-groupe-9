from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.menu_joueur_vue import MenuJoueurVue
from view.menu_table_vue import MenuTableVue

from service.joueur_service import JoueurService
from service.table_service import TableService



class MenuRejoindreTableVue(VueAbstraite):
    """
    Vue du menu du joueur pour rejoindre une table
    """

    def __init__(self, tables):
        super().__init__()
        self.tables = tables

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

        pseudo = Session().joueur

        match choix:
            case "1":
                table = TableService().rejoindre_table(pseudo, 1)
                if table == 1:
                    message = "Vous avez rejoint la table 1"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déja à la table 1"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 1"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)
                

            case "2":
                table = TableService().rejoindre_table(pseudo, 2)
                if table == 1:
                    message = "Vous avez rejoint la table 2"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déja à la table 2"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 2"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)
            
            case "3":
                table = TableService().rejoindre_table(pseudo, 3)
                if table == 1:
                    message = "Vous avez rejoint la table 3"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déja à la table 3"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 3"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)
            
            case "4":
                table = TableService().rejoindre_table(pseudo, 4)
                if table == 1:
                    message = "Vous avez rejoint la table 4"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déja à la table 4"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 4"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)

            case "5":
                table = TableService().rejoindre_table(pseudo, 5)
                if table == 1:
                    message = "Vous avez rejoint la table 5"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déja à la table 5"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 5"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)

            case "6":
                table = TableService().rejoindre_table(pseudo, 6)
                if table == 1:
                    message = "Vous avez rejoint la table 6"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déjà à la table 6"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 6"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)

            case "7":
                table = TableService().rejoindre_table(pseudo, 7)
                if table == 1:
                    message = "Vous avez rejoint la table 7"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déjà à la table 7"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 7"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)

            case "8":
                table = TableService().rejoindre_table(pseudo, 8)
                if table == 1:
                    message = "Vous avez rejoint la table 8"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déjà à la table 8"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 8"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)

            case "9":
                table = TableService().rejoindre_table(pseudo, 9)
                if table == 1:
                    message = "Vous avez rejoint la table 9"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déjà à la table 9"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 9"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)

            case "10":
                table = TableService().rejoindre_table(pseudo, 10)
                if table == 1:
                    message = "Vous avez rejoint la table 10"
                    return MenuTableVue(message, self.tables)
                elif table == 2:
                    message = "Vous êtes déjà à la table 10"
                    return MenuTableVue(message, self.tables)
                elif table == 3:
                    message = "Il n'y a plus de place à la table 10"
                    return MenuRejoindreTableVue(message, self.tables)
                else:
                    message = "La table n'existe pas"
                    return MenuRejoindreTableVue(message, self.tables)


            case "Retour":
                return MenuJoueurVue(self.tables)