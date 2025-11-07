from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.dao.joueur_dao import JoueurDao 
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
    portefeuille: int
    code_parrainage: str


# Endpoint POST /joueurs/login
@router.post("/connexion", response_model=JoueurSortie)
def connexion_joueur(payload: JoueurConnexion):
    """
    Endpoint de connexion d'un joueur.
    Vérifie le pseudo et le mot de passe dans la base SQL.
    """

    dao = JoueurDao()
    joueur = dao.trouver_par_pseudo(payload.pseudo)

    # Cas où le joueur est inconnu
    if not joueur:
        raise HTTPException(status_code=404, detail="Joueur inconnu")

    # Vérifie le mot de passe haché
    hashed_input = hash_password(payload.mdp, payload.pseudo)
    if joueur["mdp"] != hashed_input:
        raise HTTPException(status_code=401, detail="Mot de passe incorrect")

    # Cas où la connexion réussie
    return JoueurSortie(
        pseudo=joueur["pseudo"],
        code_parrainage=joueur["code_parrainage"],
        portefeuille=joueur["portefeuille"]
    )


# Endpoint POST /joueurs/inscription
@router.post("/inscription", response_model=JoueurSortie)
def inscription_joueur(payload: JoueurInscription):
    """
    Endpoint d'inscription d'un joueur.
    Crée le joueur dans la base de données SQL à partir des informations rentrées par le joueur.
    """
    code_parrainage = payload.code_parrainage
    if code_parrainage is None or code_parrainage == "":
        joueur = JoueurService().creer_sans_code_parrainage(payload.pseudo, payload.mdp)
    elif not JoueurService().code_valide(code_parrainage):
        raise HTTPException(status_code=401, detail="Code de parrainage non valide")
    else:
        joueur = JoueurService().creer(payload.pseudo, payload.mdp, payload.code_parrainage)
    return JoueurSortie(
        pseudo=joueur["pseudo"],
        code_parrainage=joueur["code_parrainage"],
        portefeuille=joueur["portefeuille"]
    )
