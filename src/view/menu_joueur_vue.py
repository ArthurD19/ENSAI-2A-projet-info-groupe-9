from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import JoueurService


class MenuJoueurVue(VueAbstraite):
    """Vue du menu du joueur

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
        """Choix du menu suivant de l'utilisateur

        Return
        ------
        vue
            Retourne la vue choisie par l'utilisateur dans le terminal
        """

        print("\n" + "-" * 50 + "\nMenu Joueur\n" + "-" * 50 + "\n")

        choix = inquirer.select(
            message="Faites votre choix : ",
            choices=[
                "Rejoindre une table",
                "Afficher la valeur du portefeuille",
                "Afficher le classement",
                "Générer un code de parrainage",
                "Se déconnecter",
            ],
        ).execute()

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue

                return AccueilVue()

            case "Afficher la valeur du portefeuille":
                portefeuille = JoueurService().afficher_valeur_portefeuille(pseudo)
                return MenuJoueurVue(portefeuille)

            case "Afficher le classement":
                classement_joueur = JoueurService().afficher_classement_joueur(pseudo)
                return MenuJoueurVue(classement_joueur)

            case "Générer un code de parrainage":
                code_parrainage = JoueurService().generer_code_parrainage(pseudo)
                return MenuJoueurVue(code_parrainage)

            case "Rejoindre une table":
                from view.menu_rejoindre_table_vue import MenuRejoindreTableVue
                return MenuRejoindreTableVue()
