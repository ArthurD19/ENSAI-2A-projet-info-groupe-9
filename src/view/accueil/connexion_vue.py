from InquirerPy import inquirer

from view.vue_abstraite import VueAbstraite
from view.session import Session

from service.joueur_service import JoueurService


class ConnexionVue(VueAbstraite):
    """Vue de Connexion (saisie de pseudo et mdp)"""

    def __init__(self, titre, tables):
        super().__init__(titre)
        self.tables = tables

    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo et mot de passe
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

        # Appel du service pour se connecter
        connecte, res = JoueurService().se_connecter(pseudo, mdp)

        if connecte:
            # Connexion réussie
            from view.menu_joueur_vue import MenuJoueurVue
            Session().connexion(res["pseudo"])  # stocke le pseudo
            message = f"Vous êtes connecté sous le pseudo {pseudo}"
            return MenuJoueurVue(message, self.tables)
        else:
            # Connexion échouée (pseudo/mot de passe invalide ou déjà connecté)
            from view.accueil.accueil_vue import AccueilVue
            # res contient déjà le message d'erreur fourni par le service
            return AccueilVue(res, self.tables)
