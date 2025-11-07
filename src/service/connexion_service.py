from utils.log_decorator import log
from utils.securite import hash_password
from dao.joueur_dao import JoueurDao
from view.session import Session

class ConnexionService:
    """Service dédié à la connexion et déconnexion des joueurs"""

    @log
    def se_connecter(self, pseudo: str, mdp: str) -> tuple[bool, str | dict]:
        """
        Authentifie un joueur.
        Retourne un tuple (succès: bool, message ou joueur: str|dict)
        """
        hashed = hash_password(mdp, pseudo)
        joueur = JoueurDao().se_connecter(pseudo, hashed)

        if joueur == "DEJA_CONNECTE":
            return False, "Vous êtes déjà connecté avec ce pseudo."
        elif joueur:
            Session().connexion(joueur["pseudo"])
            return True, joueur
        else:
            return False, "Pseudo ou mot de passe invalide."

    @log
    def se_deconnecter(self, pseudo: str) -> bool:
        """
        Déconnecte le joueur :
        - met connecte = FALSE en base
        - vide la session locale
        Retourne True si la déconnexion a bien été appliquée
        """
        result = JoueurDao().deconnecter(pseudo)
        Session().deconnexion()  # Toujours nettoyer la session locale
        return result