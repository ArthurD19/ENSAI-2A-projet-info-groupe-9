from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.joueurs import Joueur
from dao.joueur_dao import JoueurDao
from utils.genere_code_parrainage import GenerateurDeCode

from view.session import Session


class JoueurService:
    """Classe contenant les méthodes de service des Joueurs"""

    @log
    def creer(self, pseudo_joueur, mdp, code_parrain) -> Joueur:
        """Création d'un joueur à partir de ses attributs"""

        nouveau_joueur = {
            "pseudo": pseudo_joueur,
            "mdp": hash_password(mdp, pseudo_joueur),
            "portefeuille": 1000,
            "code_parrainage": None,
            # la colonne 'connecte' a une valeur par défaut en base (FALSE)
        }

        if JoueurDao().creer(nouveau_joueur):
            if code_parrain:
                if JoueurDao().code_de_parrainage_existe(code_parrain):
                    parrain = JoueurDao().trouver_par_code_parrainage(code_parrain)
                    parrain["portefeuille"] = parrain["portefeuille"] + 20
                    nouveau_joueur["portefeuille"] = nouveau_joueur["portefeuille"] + 100
                    modif_nouveau_joueur = JoueurDao().modifier(nouveau_joueur)
                    modif_parrain = JoueurDao().modifier(parrain)
                    if modif_nouveau_joueur and modif_parrain:
                        return nouveau_joueur
                return nouveau_joueur
        else:
            return None

    @log
    def creer_sans_code_parrainage(self, pseudo_joueur, mdp) -> Joueur:
        """Création d'un joueur à partir de ses attributs"""

        nouveau_joueur = {
            "pseudo": pseudo_joueur,
            "mdp": hash_password(mdp, pseudo_joueur),
            "portefeuille": 1000,
            "code_parrainage": None,
        }

        if JoueurDao().creer(nouveau_joueur):
            return nouveau_joueur
        else:
            return None

    @log
    def lister_tous(self, inclure_mdp=False) -> list[Joueur]:
        """Lister tous les joueurs
        Si inclure_mdp=True, les mots de passe seront inclus
        Par défaut, tous les mdp des joueurs sont à None
        """
        joueurs = JoueurDao().lister_tous()
        if not inclure_mdp:
            for j in joueurs:
                # si j est un dict (issue du DAO), on met la clé mdp à None
                try:
                    j["mdp"] = None
                except Exception:
                    # si j est un business object Joueur
                    try:
                        j.mdp = None
                    except Exception:
                        pass
        return joueurs

    @log
    def trouver_par_id(self, id_joueur) -> Joueur:
        """Trouver un joueur à partir de son id
        """
        return JoueurDao().trouver_par_id(id_joueur)

    @log
    def modifier(self, joueur) -> Joueur:
        """Modification d'un joueur"""

        # si joueur est un dict ou un objet, on récupère le pseudo et le mdp
        try:
            pseudo = joueur["pseudo"]
            mdp = joueur["mdp"]
            joueur["mdp"] = hash_password(mdp, pseudo)
        except Exception:
            # objet business
            joueur.mdp = hash_password(joueur.mdp, joueur.pseudo)

        return joueur if JoueurDao().modifier(joueur) else None

    @log
    def supprimer(self, joueur) -> bool:
        """Supprimer le compte d'un joueur"""
        return JoueurDao().supprimer(joueur)

    @log
    def afficher_tous(self) -> str:
        """Afficher tous les joueurs
        Sortie : Une chaine de caractères mise sous forme de tableau
        """
        entetes = ["pseudo", "age", "mail", "est fan de Pokemon"]

        joueurs = JoueurDao().lister_tous()

        # On tente d'enlever l'admin si présent
        for j in list(joueurs):
            try:
                if (isinstance(j, dict) and j.get("pseudo") == "admin") or getattr(j, "pseudo", None) == "admin":
                    joueurs.remove(j)
            except Exception:
                pass

        joueurs_as_list = []
        for j in joueurs:
            try:
                # si business object
                joueurs_as_list.append(j.as_list())
            except Exception:
                # s'il s'agit d'un dict depuis le DAO
                joueurs_as_list.append([j.get("pseudo"), j.get("mdp"), j.get("portefeuille"), j.get("code_parrainage")])

        str_joueurs = "-" * 100
        str_joueurs += "\nListe des joueurs \n"
        str_joueurs += "-" * 100
        str_joueurs += "\n"
        str_joueurs += tabulate(
            tabular_data=joueurs_as_list,
            headers=entetes,
            tablefmt="psql",
            floatfmt=".2f",
        )
        str_joueurs += "\n"

        return str_joueurs

    @log
    def se_connecter(self, pseudo, mdp) -> tuple[bool, str | dict]:
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
    def se_deconnecter(self, pseudo) -> bool:
        """
        Déconnecte le joueur : met connecte = FALSE en base et vide la session locale.
        Retourne True si la déconnexion a bien été appliquée en base.
        """
        result = JoueurDao().deconnecter(pseudo)
        if result:
            try:
                Session().deconnexion()
            except Exception:
                pass
        return result

    @log
    def pseudo_deja_utilise(self, pseudo) -> bool:
        """Vérifie si le pseudo est déjà utilisé
        Retourne True si le pseudo existe déjà en BDD"""
        return JoueurDao().pseudo_existe(pseudo)

    @log
    def afficher_valeur_portefeuille(self, pseudo):
        return JoueurDao().valeur_portefeuille(pseudo)

    @log
    def afficher_classement_joueur(self, pseudo):
        return JoueurDao().classement_par_portefeuille()

    @log
    def generer_code_parrainage(self, pseudo):
        joueur = JoueurDao().trouver_par_pseudo(pseudo)
        if not joueur:
            return None
        if not joueur.get('code_parrainage') or str(joueur['code_parrainage']).strip() == "":
            code = GenerateurDeCode().generate_unique_code()
            maj_ok = JoueurDao().mettre_a_jour_code_de_parrainage(pseudo, code)
            if maj_ok:
                return code
            else:
                return "code non genere"
        else:
            return joueur['code_parrainage']

    @log
    def code_valide(self, code_parrainage):
        return JoueurDao().code_de_parrainage_existe(code_parrainage)

    @log
    def rejoindre_table(self, pseudo: str, num_table: str):
        # on la codera une fois qu'on saura comment gérer les tables
        pass
