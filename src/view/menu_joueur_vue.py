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
                "Générer ou voir mon code de parrainage",
                "Se déconnecter",
            ],
        ).execute()

        pseudo = Session().joueur

        match choix:
            case "Se déconnecter":
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue
                print("\nVous êtes maintenant déconnecté.\n")
                return AccueilVue()

            case "Afficher la valeur du portefeuille":
                portefeuille = JoueurService().afficher_valeur_portefeuille(pseudo)
                print(f"\nVotre portefeuille contient : {portefeuille} jetons.\n")
                input("Appuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue()

            case "Afficher le classement":
                classement_joueur = JoueurService().afficher_classement_joueur(pseudo)
                print("\nVotre position actuelle dans le classement :")
                print(classement_joueur)
                input("\nAppuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue()

            case "Générer ou voir mon code de parrainage":
                code_parrainage = JoueurService().generer_code_parrainage(pseudo)
                print(f"\nVotre code de parrainage est : {code_parrainage}\n")
                input("Appuyez sur Entrée pour revenir au menu parrainage.")
                return MenuJoueurVue()

            case "Rejoindre une table":
                from view.menu_rejoindre_table_vue import MenuRejoindreTableVue
                return MenuRejoindreTableVue()
