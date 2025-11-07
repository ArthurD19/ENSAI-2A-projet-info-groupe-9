from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.dao.joueur_dao import JoueurDao 
from src.dao.statistique_dao import StatistiqueDao
from src.service.joueur_service import JoueurService
from src.service.partie_service import PartieService

router = APIRouter(prefix="/joueur_en_jeu", tags=["joueur_en_jeu"])

# Modèle de sortie (réponse renvoyée)
class JoueurConnecte(BaseModel):
    pseudo: str
    portefeuille: int
    code_parrainage: str


# Endpoint POST /joueur_en_jeu/miser
@router.post("/miser", response_model=str)
def miser_joueur(payload: JoueurConnecte, montant: int):
    """
    Endpoint de l'action miser pour un joueur.
    Vérifie si le joueur peut miser le montant qu'il souhaite et le fait si possible.
    """

    joueur = payload.pseudo
    fait, message = PartieService().miser(joueur, montant)
    if fait : 
        return "Action effectuée"
    else:
        return message


# Endpoint POST /joueur_en_jeu/se_coucher
@router.post("/se_coucher", response_model=str)
def se_coucher_joueur(payload: JoueurConnecte):
    """
    Endpoint de l'action se coucher pour un joueur.
    """

    joueur = payload.pseudo
    fait, message = PartieService().se_coucher(joueur)
    if fait : 
        return "Action effectuée"
    else:
        return message


# Endpoint POST /joueur_en_jeu/suivre
@router.post("/suivre", response_model=str)
def suivre_joueur(payload: JoueurConnecte):
    """
    Endpoint de l'action de suivre pour un joueur.
    Vérifie si le joueur peut miser le montant qu'il souhaite et le fait si possible.
    """

    joueur = payload.pseudo
    fait, message = PartieService().suivre(joueur)
    if fait : 
        return "Action effectuée"
    else:
        return message


# Endpoint POST /joueur_en_jeu/all_in
@router.post("/all_in", response_model=str)
def all_in_joueur(payload: JoueurConnecte):
    """
    Endpoint de l'action all_in pour un joueur.
    Vérifie si le joueur peut miser le montant qu'il souhaite et le fait si possible.
    """

    joueur = payload.pseudo
    fait, message = PartieService().all_in(joueur)
    if fait : 
        return "Action effectuée"
    else:
        return message


# Endpoint POST /joueur_en_jeu/voir_etat_partie
@router.post("/voir_etat_partie", response_model=str)
def voir_etat_partie():
    """
    Endpoint de l'action voir état de la partie pour un joueur.
    Renvoie l'état de la partie.
    """

    joueur = payload.pseudo
    fait, message = PartieService().voir_etat_partie()
    if fait : 
        return "Action effectuée"
    else:
        return message