import os

import regex
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, PasswordValidator
from prompt_toolkit.validation import ValidationError, Validator

from service.joueur_service import JoueurService
from view.vue_abstraite import VueAbstraite


class InscriptionVue(VueAbstraite):
    def choisir_menu(self):
        # Demande à l'utilisateur de saisir pseudo, mot de passe...
        pseudo = inquirer.text(message="Entrez votre pseudo : ").execute()

        if JoueurService().pseudo_deja_utilise(pseudo):
            from view.accueil.accueil_vue import AccueilVue

            return AccueilVue(f"Le pseudo {pseudo} est déjà utilisé.")

        mdp = inquirer.secret(
            message="Entrez votre mot de passe : ",
            validate=PasswordValidator(
                length=os.environ["PASSWORD_LENGTH"],
                cap=True,
                number=True,
                message="Au moins 16 caractères, incluant une majuscule et un chiffre",
            ),
        ).execute()

        code_de_parrainage = inquirer.text(message="Entrez un code de parrainage : ").execute()

        # Appel du service pour créer le joueur
        joueur = JoueurService().creer(pseudo, mdp, code_de_parrainage)

        # Si le joueur a été créé
        if joueur:
            message = (
                f"Votre compte {joueur.pseudo} a été créé. Vous pouvez maintenant vous connecter."
            )
        else:
            message = "Erreur de connexion (pseudo ou mot de passe invalide)"

        from view.accueil.accueil_vue import AccueilVue

        return AccueilVue(message)

