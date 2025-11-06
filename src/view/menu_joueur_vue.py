from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import JoueurService
from service.statistique_service import StatistiqueService


class MenuJoueurVue(VueAbstraite):
    """
    Vue du menu du joueur
    """

    def __init__(self, titre, tables):
        super().__init__(titre)
        self.tables = tables

    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur"""
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

        pseudo = Session().joueur  # doit être une chaîne (le pseudo)

        match choix:
            case "Se déconnecter":
                # Appeler le service pour mettre connecte = FALSE en base
                try:
                    JoueurService().se_deconnecter(pseudo)
                except Exception:
                    # on ignore l'erreur et on poursuit la déconnexion locale
                    pass
                Session().deconnexion()
                from view.accueil.accueil_vue import AccueilVue
                message = "Vous êtes maintenant déconnecté."
                return AccueilVue(message, self.tables)

            case "Afficher la valeur du portefeuille":
                portefeuille = JoueurService().afficher_valeur_portefeuille(pseudo)
                print(f"\nVotre portefeuille contient : {portefeuille} jetons.\n")
                input("Appuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue("", self.tables)

            case "Afficher le classement":
                classement_joueur = JoueurService().afficher_classement_joueur(pseudo)

                print("\nClassement des joueurs :")
                print("-" * 40)

                if not classement_joueur:
                    print("Aucun joueur trouvé.")
                else:
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
                input("\nAppuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue("", self.tables)

            case "Afficher les statistiques":
                stats = StatistiqueService().afficher_statistiques_joueur(pseudo)
                print("\nVos statistiques :")
                print("-" * 50)
                if not stats:
                    print("Aucune statistique disponible.")
                else:
                    # j'affiche clef prettifiée et la valeur ; j'ignore les valeurs None
                    for champ, valeur in stats.items():
                        if valeur is None:
                            continue
                        # remplacer _ par espace et mettre en minuscule puis capitaliser
                        label = champ.replace("_", " ").capitalize()
                        print(f"{label:<30} : {valeur}")
                print("-" * 50)
                input("\nAppuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue("", self.tables)

            case "Générer ou voir mon code de parrainage":
                code_parrainage = JoueurService().generer_code_parrainage(pseudo)
                print(f"\nVotre code de parrainage est : {code_parrainage}\n")
                input("Appuyez sur Entrée pour revenir au menu précédent.")
                return MenuJoueurVue("", self.tables)

            case "Rejoindre une table":
                from view.menu_rejoindre_table_vue import MenuRejoindreTableVue
                return MenuRejoindreTableVue(self.tables)
