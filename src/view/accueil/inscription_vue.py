import os
from InquirerPy import inquirer
from InquirerPy.validator import PasswordValidator

from service.joueur_service import JoueurService
from view.vue_abstraite import VueAbstraite


class InscriptionVue(VueAbstraite):

    def __init__(self, titre, tables):
        super().__init__(titre)
        self.tables = tables

    def choisir_menu(self):
        """Demande à l'utilisateur pseudo, mot de passe et code de parrainage, puis crée le joueur"""

        # Récupérer la longueur de mot de passe minimale depuis l'environnement
        length = int(os.environ.get("PASSWORD_LENGTH", 8))

        # Demande du pseudo
        pseudo = inquirer.text(
            message="Entrez votre pseudo : "
        ).execute()

        # Vérifier que le pseudo n'est pas déjà utilisé
        if JoueurService().pseudo_deja_utilise(pseudo):
            from view.accueil.accueil_vue import AccueilVue
            return AccueilVue(f"Le pseudo '{pseudo}' est déjà utilisé.", self.tables)

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
        code_de_parrainage = inquirer.text(
            message="Entrez un code de parrainage (facultatif) : "
        ).execute().strip()

        # Création du joueur selon la présence ou non du code de parrainage
        if code_de_parrainage:
            if JoueurService().code_valide(code_de_parrainage):
                joueur = JoueurService().creer(pseudo, mdp, code_de_parrainage)
            else:
                from view.accueil.accueil_vue import AccueilVue
                return AccueilVue("Code de parrainage non valide.", self.tables)
        else:
            joueur = JoueurService().creer_sans_code_parrainage(pseudo, mdp)

        # Vérifier si le joueur a été créé
        if joueur:
            message = f"Votre compte '{joueur['pseudo']}' a été créé. Vous pouvez maintenant vous connecter."
        else:
            message = "Erreur lors de la création du compte. Vérifiez vos informations."

        from view.accueil.accueil_vue import AccueilVue
        return AccueilVue(message, self.tables)
