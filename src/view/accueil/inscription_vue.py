# src/view/accueil/inscription_vue.py
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator
from src.view.vue_abstraite import VueAbstraite
from src.view.session import Session
from src.client.api_client import post, APIError
from src.service.joueur_service import JoueurService
import os

class InscriptionVue(VueAbstraite):
    def __init__(self, titre, tables):
        super().__init__(titre)
        self.tables = tables

    def choisir_menu(self):
        """Demande pseudo, mot de passe et code de parrainage, puis crée le joueur via API"""

        # Récupérer la longueur de mot de passe minimale depuis l'environnement
        length = int(os.environ.get("PASSWORD_LENGTH", 8))

        # Demande du pseudo
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()

        # Demande du mot de passe avec validation
        mdp = inquirer.secret(
            message=f"Entrez votre mot de passe (au moins {length} caractères, 1 majuscule et 1 chiffre) : ",
            validate=PasswordValidator(
                length=length,
                cap=True,
                number=True,
                message=f"Le mot de passe doit contenir au moins {length} caractères, 1 majuscule et 1 chiffre."
            )
        ).execute()

        # Demande du code de parrainage (facultatif)
        code_parrainage = inquirer.text(
            message="Entrez un code de parrainage (optionnel) :",
            default=""
        ).execute().strip()

        payload = {
            "pseudo": pseudo,
            "mdp": mdp,
            "code_parrainage": code_parrainage or None
        }

        try:
            # Appel HTTP POST à l'API
            res = post("/joueurs/inscription", json=payload)
            
            # Connexion automatique après création
            Session().connexion(res["pseudo"])
            JoueurService().se_connecter(res["pseudo"], mdp)
            message = f"Compte créé et connecté sous le pseudo {res['pseudo']}"

            # Passage au menu joueur
            from src.view.menu_joueur_vue import MenuJoueurVue
            return MenuJoueurVue(message, self.tables)

        except APIError as e:
            msg = str(e)
            if "400" in msg or "Code de parrainage non valide" in msg:
                message = "Erreur : code de parrainage invalide"
            elif "409" in msg or "déjà utilisé" in msg.lower():
                message = "Erreur : pseudo déjà utilisé"
            else:
                message = f"Erreur réseau/API : {msg}"

            from src.view.accueil.accueil_vue import AccueilVue
            return AccueilVue(message, self.tables)
