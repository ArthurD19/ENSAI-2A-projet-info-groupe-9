from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.dao.joueur_dao import JoueurDao 
from src.dao.statistique_dao import StatistiqueDao
from src.utils.securite import hash_password
from src.service.joueur_service import JoueurService

router = APIRouter(prefix="/joueurs", tags=["joueurs"])


# Modèle d’entrée (JSON reçu du client)
class JoueurConnexion(BaseModel):
    pseudo: str
    mdp: str


# Modèle de sortie (réponse renvoyée)
class JoueurSortie(BaseModel):
    pseudo: str
    code_parrainage: str | None = None
    portefeuille: float


# Modèle de sortie (réponse renvoyée)
class JoueurInscription(BaseModel):
    pseudo: str
    mdp: str
    code_parrainage: str | None = None


# Modèle de sortie (réponse renvoyée)
class JoueurConnecte(BaseModel):
    pseudo: str


# Endpoint POST /joueurs/login
@router.post("/connexion", response_model=JoueurSortie)
def connexion_joueur(payload: JoueurConnexion):
    """
    Endpoint de connexion d'un joueur.
    Vérifie le pseudo et le mot de passe dans la base SQL.
    """

    dao = JoueurDAO()
    joueur = dao.find_by_pseudo(payload.pseudo)

    # Cas où le joueur est inconnu
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur inconnu")

    # Vérifie le mot de passe haché
    hashed_input = hash_password(payload.mdp, payload.pseudo)
    if joueur.mdp != hashed_input:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    # Cas où la connexion réussie
    return JoueurOut(
        pseudo=joueur.pseudo,
        code_parrainage=joueur.code_parrainage,
        portefeuille=joueur.portefeuille
    )


# Endpoint POST /joueurs/inscription
@router.post("/inscription", response_model=JoueurSortie)
def inscription_joueur(payload: JoueurInscription):
    """
    Endpoint d'inscription d'un joueur.
    Crée le joueur dans la base de données SQL à partir des informations rentrées par le joueur.
    """

    dao = JoueurDAO()
    code_parrainage = payload.code_parrainage
    if code_parrainage is None or code_parrainage == "":
        joueur = JoueurService().creer_sans_code_parrainage(payload.pseudo, payload.mdp)
    elif not JoueurService().code_valide(code_parrainage):
        raise HTTPException(status_code=401, detail="Code de parrainage non valide")
    else:
        joueur = JoueurService().creer(payload.pseudo, payload.mdp, payload.code_parrainage)
    return JoueurOut(
        pseudo=joueur.pseudo,
        code_parrainage=joueur.code_parrainage,
        portefeuille=joueur.portefeuille
    )


# Endpoint GET /joueurs/code_parrainage
@router.get("/code_parrainage", response_model=str)
def code_parrainage_joueur(payload: JoueurConnecte):
    """
    Endpoint de récupération de son code de parrainage par un joueur.
    Vérifie si un code de parrainage existe dans la base SQL, le renvoie dans ce cas et sinon crée
    le code de parrainage.
    """

    joueur = JoueurDao().trouver_par_pseudo(payload.pseudo)
    
    if not joueur:
        raise HTTPException(status_code=401, detail="Pseudo inconnu")
    if joueur.code_parrainage is not None:
        code = JoueurService().generer_code_parrainage(payload.pseudo)
        return code
    else:
        return joueur.code_parrainage


# Endpoint GET /joueurs/stats
@router.get("/stats", response_model=dict)
def stats_joueur(payload: JoueurConnecte):
    """
    Endpoint de récupération de ses statistiques par un joueur.
    """

    statistiques = StatistiqueDao().trouver_statistiques_par_id(payload.pseudo)
    
    if statistiques == {}:
        raise HTTPException(status_code=401, detail="Joueur inconnu ou n'ayant pas de statistiques")
    else:
        return statistiques


# Endpoint GET /joueurs/valeur_portefeuille
@router.get("/valeur_portefeuille", response_model=int)
def portefeuille_joueur(payload: JoueurConnecte):
    """
    Endpoint de récupération de la valeur de son portefeuille par un joueur.
    """

    valeur = JoueurDao().valeur_portefeuille(payload.pseudo)
    
    if valeur is not None:
        return valeur
    else:
        raise HTTPException(status_code=401, detail="Pseudo inconnu")


# Endpoint GET /joueurs/voir_classement
@router.get("/voir_classement", response_model=dict)
def voir_classement_joueur(payload: JoueurConnecte):
    """
    Endpoint de récupération de la valeur de son portefeuille par un joueur.
    """

    classement = JoueurDao().classement_par_portefeuille(limit=None)
    return classement

# Faire tous les autres