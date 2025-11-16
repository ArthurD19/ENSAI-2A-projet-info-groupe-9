from fastapi import APIRouter, Depends, HTTPException

from pydantic import BaseModel

from dao.joueur_dao import JoueurDao 
from dao.statistique_dao import StatistiqueDao

from service.joueur_service import JoueurService
from service.partie_service import PartieService
from service.table_service import TableService

from business_object.partie import EtatPartie
from business_object.cartes import Carte

from api.var_utiles import tables_service

router = APIRouter(prefix="/joueur_en_jeu", tags=["joueur_en_jeu"])

# Modèle d'entrée pour le joueur ayant rejoint une partie (réponse renvoyée)
class JoueurEnJeu(BaseModel):
    pseudo: str
    portefeuille: int
    partie: int

# Modèle de sortie pour la partie
class RetourPartie(BaseModel):
    id_partie: int
    tour_actuel: str
    joueurs: list[dict]          # contient : pseudo, solde, mise, actif
    board: list[str]
    pot: int
    pots_secondaires: dict
    mise_max: int
    joueur_courant: str | None 
    finie: bool                # True si la partie est terminée
    resultats: list[dict]       # liste des gagnants avec info sur leur main et kickers
    rejouer: dict[str, bool | None]
    liste_attente: list[dict] 
    message_retour: str


# Endpoint POST /joueur_en_jeu/miser
@router.post("/miser", response_model=RetourPartie)
def miser_joueur(payload: JoueurEnJeu, montant: int, partie: int):
    """
    Endpoint de l'action miser pour un joueur.
    Vérifie si le joueur peut miser le montant qu'il souhaite et le fait si possible.
    """

    joueur = payload.pseudo
    partie_jouee = tables_service.parties[partie]
    partie_jouee_service = PartieService(partie_jouee)
    fait, etat_partie, message = partie_jouee_service.miser(joueur, montant)
    if fait : 
        message = "Action effectuée"
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,       
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             
            resultats = etat_partie.resultats,     
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour
    else:
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,        # contient : pseudo, solde, mise, actif
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             # True si la partie est terminée
            resultats = etat_partie.resultats,      # liste des gagnants avec info sur leur main et kickers
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour


# Endpoint POST /joueur_en_jeu/se_coucher
@router.post("/se_coucher", response_model=RetourPartie)
def se_coucher_joueur(payload: JoueurEnJeu, partie: int):
    """
    Endpoint de l'action se coucher pour un joueur.
    """

    joueur = payload.pseudo
    partie_jouee = tables_service.parties[partie]
    partie_jouee_service = PartieService(partie_jouee)
    fait, etat_partie, message = partie_jouee_service.se_coucher(joueur)
    if fait : 
        message = "Action effectuée"
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,       
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             
            resultats = etat_partie.resultats,     
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour
    else:
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,        # contient : pseudo, solde, mise, actif
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             # True si la partie est terminée
            resultats = etat_partie.resultats,      # liste des gagnants avec info sur leur main et kickers
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour

# Endpoint POST /joueur_en_jeu/suivre
@router.post("/suivre", response_model=RetourPartie)
def suivre_joueur(payload: JoueurEnJeu, partie: int):
    """
    Endpoint de l'action de suivre pour un joueur.
    Vérifie si le joueur peut miser le montant qu'il souhaite et le fait si possible.
    """

    joueur = payload.pseudo
    partie_jouee = tables_service.parties[partie]
    partie_jouee_service = PartieService(partie_jouee)
    fait, etat_partie, message = partie_jouee_service.suivre(joueur)
    if fait : 
        message = "Action effectuée"
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,       
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             
            resultats = etat_partie.resultats,     
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour
    else:
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,        # contient : pseudo, solde, mise, actif
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             # True si la partie est terminée
            resultats = etat_partie.resultats,      # liste des gagnants avec info sur leur main et kickers
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour


# Endpoint POST /joueur_en_jeu/all_in
@router.post("/all_in", response_model=RetourPartie)
def all_in_joueur(payload: JoueurEnJeu, partie: int):
    """
    Endpoint de l'action all_in pour un joueur.
    Vérifie si le joueur peut miser le montant qu'il souhaite et le fait si possible.
    """

    joueur = payload.pseudo
    partie_jouee = tables_service.parties[partie]
    partie_jouee_service = PartieService(partie_jouee)
    fait, etat_partie, message = partie_jouee_service.all_in(joueur)
    partie_jouee.etat = etat_partie
    if fait : 
        message = "Action effectuée"
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,       
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             
            resultats = etat_partie.resultats,     
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour
    else:
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,        # contient : pseudo, solde, mise, actif
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             # True si la partie est terminée
            resultats = etat_partie.resultats,      # liste des gagnants avec info sur leur main et kickers
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour


# Endpoint GET /joueur_en_jeu/voir_etat_partie
@router.get("/voir_etat_partie", response_model=RetourPartie)
def voir_etat_partie(partie: int):
    """
    Endpoint de l'action voir état de la partie pour un joueur.
    Renvoie l'état de la partie.
    """
    partie_jouee = tables_service.parties[partie]
    partie_jouee_service = PartieService(partie_jouee)
    fait, etat_partie, message = partie_jouee_service.voir_etat_partie()
    if fait : 
        message = "Action effectuée"
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,       
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             
            resultats = etat_partie.resultats,     
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour
    else:
        partie_retour = RetourPartie(
            id_partie = etat_partie.id_partie,
            tour_actuel = etat_partie.tour_actuel,
            joueurs = etat_partie.joueurs,        # contient : pseudo, solde, mise, actif
            board = etat_partie.board,
            pot = etat_partie.pot,
            pots_secondaires = etat_partie.pots_secondaires,
            mise_max = etat_partie.mise_max,
            joueur_courant = etat_partie.joueur_courant,
            finie = etat_partie.finie,             # True si la partie est terminée
            resultats = etat_partie.resultats,      # liste des gagnants avec info sur leur main et kickers
            rejouer = etat_partie.rejouer,
            liste_attente = etat_partie.liste_attente, 
            message_retour = message
        )
        return partie_retour

# Endpoint GET /joueur_en_jeu/voir_mes_cartes
@router.get("/voir_mes_cartes", response_model=str)
def voir_mes_cartes(partie: int, pseudo: str):
    """
    Endpoint pour que le joueur puisse voir ses cartes.
    Renvoie la liste des cartes du joueur.
    """
    table = tables_service.tables[partie]
    for j in table.joueurs:
        if j.pseudo == pseudo:
            liste_cartes = [str(c) for c in j.main]
            main = liste_cartes[0] + liste_cartes[1]
            return main
    return "Le joueur n'a pas été trouvé à la table"


# Endpoint POST /joueur_en_jeu/quitter_table
@router.post("/quitter_table", response_model=str)
def quitter_table_joueur(pseudo: str, id_table: int):
    """
    Endpoint permettant à un joueur de quitter une table.
    """
    quitter = tables_service.quitter_table(pseudo, id_table)
    if quitter == 1: 
        return "Table quittée"
    else:
        return "Joueur non supprimé (non présent certainement)"