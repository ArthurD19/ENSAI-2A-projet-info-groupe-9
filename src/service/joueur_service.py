from tabulate import tabulate

from utils.log_decorator import log
from utils.securite import hash_password

from business_object.joueurs import Joueur
from dao.joueur_dao import JoueurDao
from utils.genere_code_parrainage import GenerateurDeCode


class JoueurService:
    """Classe contenant les méthodes de service des Joueurs"""

    @log
    def creer(self, pseudo_joueur, mdp, code_parrain) -> Joueur:
        """Création d'un joueur à partir de ses attributs"""

        nouveau_joueur = {
            "pseudo": pseudo_joueur,
            "mdp": hash_password(mdp, pseudo_joueur),
            "portefeuille": 1000, 
            "code_parrainage": None}

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
            None

    @log
    def creer_sans_code_parrainage(self, pseudo_joueur, mdp) -> Joueur:
        """Création d'un joueur à partir de ses attributs"""

        nouveau_joueur = {
            "pseudo": pseudo_joueur,
            "mdp": hash_password(mdp, pseudo_joueur),
            "portefeuille": 1000, 
            "code_parrainage": None}

        if JoueurDao().creer(nouveau_joueur):
            return nouveau_joueur 
        else: 
            None

    @log
    def lister_tous(self, inclure_mdp=False) -> list[Joueur]:
        """Lister tous les joueurs
        Si inclure_mdp=True, les mots de passe seront inclus
        Par défaut, tous les mdp des joueurs sont à None
        """
        joueurs = JoueurDao().lister_tous()
        if not inclure_mdp:
            for j in joueurs:
                j.mdp = None
        return joueurs

    @log
    def trouver_par_id(self, id_joueur) -> Joueur:
        """Trouver un joueur à partir de son id
        
        Parameters
        ----------
        id_joueur: str
            identifiant du joueur que l'on chercher
        """
        return JoueurDao().trouver_par_id(id_joueur)

    @log
    def modifier(self, joueur) -> Joueur:
        """Modification d'un joueur"""

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

        for j in joueurs:
            if j.pseudo == "admin":
                joueurs.remove(j)

        joueurs_as_list = [j.as_list() for j in joueurs]

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
    def se_connecter(self, pseudo, mdp) -> Joueur:
        """Se connecter à partir de pseudo et mdp"""
        joueur = JoueurDao().se_connecter(pseudo, hash_password(mdp, pseudo))
        if joueur:
            return joueur
        else:
            return False

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
        if joueur['code_parrainage'] == "":
            code = GenerateurDeCode().generate_unique_code()
            maj_ok = JoueurDao().mettre_a_jour_code_de_parrainage(pseudo, code)
            if maj_ok:
                return code
            else:
                return "code non genere"
        else:
            return joueur['code_parrainage']

    @log
    def rejoindre_table(self, pseudo: str, num_table: str):
        # on la codera une fois qu'on saura comment gérer les tables
        pass
