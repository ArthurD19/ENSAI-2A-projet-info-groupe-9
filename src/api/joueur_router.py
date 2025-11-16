from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from service.joueur_service import JoueurService

router = APIRouter(prefix="/joueurs", tags=["joueurs"])


# Modèle d’entrée pour la connexion (JSON reçu du client)
class JoueurConnexion(BaseModel):
    pseudo: str
    mdp: str


# Modèle de sortie le joueur une fois inscrit ou connecté (réponse renvoyée)
class JoueurSortie(BaseModel):
    pseudo: str
    code_parrainage: str | None = None
    portefeuille: int


# Modèle d’entrée pour l'inscription
class JoueurInscription(BaseModel):
    pseudo: str
    mdp: str
    code_parrainage: str | None = None


# Endpoint POST /joueurs/connexion
@router.post("/connexion", response_model=JoueurSortie)
def connexion_joueur(payload: JoueurConnexion):
    """
    Endpoint de connexion d'un joueur.
    Utilise JoueurService.se_connecter() qui :
      - renvoie (True, joueur_dict) si connexion OK (et met connecte = TRUE en BDD)
      - renvoie (False, "message") si échec (déjà connecté ou identifiants invalides)
    """
    ok, res = JoueurService().se_connecter(payload.pseudo, payload.mdp)

    if ok:
        joueur = res
        return JoueurSortie(
            pseudo=joueur["pseudo"],
            code_parrainage=joueur.get("code_parrainage"),
            portefeuille=int(joueur["portefeuille"]),
        )

    # res est un message d'erreur
    message = str(res)
    if "déjà connecté" in message.lower() or "déja connecté" in message.lower():
        raise HTTPException(status_code=409, detail=message)
    else:
        raise HTTPException(status_code=401, detail=message)


# Endpoint POST /joueurs/inscription
@router.post("/inscription", response_model=JoueurSortie)
def inscription_joueur(payload: JoueurInscription):
    """
    Endpoint de l'inscription d'un joueur sur le serveur.
    """
    code_parrainage = payload.code_parrainage

    # Vérifie si pseudo déjà utilisé
    service = JoueurService()
    if service.pseudo_deja_utilise(payload.pseudo):
        raise HTTPException(status_code=409, detail=f"Le pseudo '{payload.pseudo}' est déjà utilisé.")

    if not code_parrainage:
        joueur = service.creer_sans_code_parrainage(payload.pseudo, payload.mdp)
    elif not service.code_valide(code_parrainage):
        raise HTTPException(status_code=400, detail="Code de parrainage non valide")
    else:
        joueur = service.creer(payload.pseudo, payload.mdp, code_parrainage)

    if not joueur:
        raise HTTPException(status_code=500, detail="Impossible de créer le joueur")

    return JoueurSortie(
        pseudo=joueur["pseudo"],
        code_parrainage=joueur.get("code_parrainage"),
        portefeuille=int(joueur["portefeuille"]),
    )



