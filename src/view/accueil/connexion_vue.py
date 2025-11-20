from InquirerPy import inquirer
from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.client.api_client import post, APIError
from src.utils.log_decorator import log


class ConnexionVue(VueAbstraite):
    def __init__(self, titre, tables):
        super().__init__(titre)
        self.tables = tables

    @log
    def choisir_menu(self):
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()
        mdp = inquirer.secret(message="Entrez votre mot de passe :").execute()

        try:
            payload = {"pseudo": pseudo, "mdp": mdp}
            res = post("/joueurs/connexion", json=payload)
            # res correspond au modèle JoueurSortie {pseudo, code_parrainage, portefeuille}
            Session().connexion(res["pseudo"])
            message = f"Vous êtes connecté sous le pseudo {res['pseudo']}"
            from src.view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue(message, self.tables)
        except APIError as e:
            # message d'erreur utile pour l'utilisateur
            msg = str(e)
            if "401" in msg or "Mot de passe incorrect" in msg:
                message = "Erreur de connexion (pseudo ou mot de passe invalide)"
            elif "404" in msg or "Joueur inconnu" in msg:
                message = "Erreur : joueur inconnu"
            else:
                message = f"Erreur réseau/API : {msg}"
            from src.view.accueil.accueil_vue import AccueilVue
            return AccueilVue(message, self.tables)
