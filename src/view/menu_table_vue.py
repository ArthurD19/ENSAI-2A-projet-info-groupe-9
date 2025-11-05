from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session
from view.menu_joueur_vue import MenuJoueurVue

from service.joueur_service import JoueurService
from service.table_service import TableService


class MenuTableVue(VueAbstraite):
    """
    Vue du menu du joueur pendant une partie
    """

    def __init__(self, titre, tables):
        super().__init__(titre)
        self.tables = tables

    def choisir_menu(self):
        table = self.tables.lister_tables()
        print(table)
        input("Appuyez sur Entrée pour revenir au menu précédent.")
        message = "retour au menu joueur"
        return MenuJoueurVue(message, self.tables)