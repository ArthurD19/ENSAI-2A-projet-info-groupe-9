from fastapi import APIRouter, Depends, HTTPException, status

from pydantic import BaseModel

from src.dao.joueur_dao import JoueurDao 
from src.dao.statistique_dao import StatistiqueDao

from src.service.joueur_service import JoueurService
from src.service.partie_service import PartieService
from src.service.table_service import TableService

from src.api.var_utiles import tables_service, scheduler

router = APIRouter(prefix="/joueur_connecte", tags=["joueur_connecte"])

# Modèle de sortie pour voir une table
class TableSortie(BaseModel):
    id: int
    nombre_joueurs: int
    blind: int
    pot: int
    indice_dealer: int

# Modèle de sortie pour rejoindre une table
class TableRejointe(BaseModel):
    succes: bool
    message: str


# Endpoint GET /joueur_connecte/code_parrainage
@router.get("/code_parrainage", response_model=str)
def code_parrainage_joueur(pseudo: str):
    """
    Endpoint de récupération de son code de parrainage par un joueur.
    Vérifie si un code de parrainage existe dans la base SQL, le renvoie dans ce cas et sinon crée
    le code de parrainage.
    """

    joueur = JoueurDao().trouver_par_pseudo(pseudo)
    
    if not joueur:
        raise HTTPException(status_code=401, detail="Pseudo inconnu")
    if joueur["code_parrainage"] is None:
        code = JoueurService().generer_code_parrainage(pseudo)
        return code
    else:
        return joueur["code_parrainage"]


# Endpoint GET /joueur_connecte/stats
@router.get("/stats", response_model=dict)
def stats_joueur(pseudo: str):
    """
    Endpoint de récupération de ses statistiques par un joueur.
    """

    statistiques = StatistiqueDao().trouver_statistiques_par_id(pseudo)
    
    if statistiques == {}:
        raise HTTPException(status_code=401, detail="Joueur inconnu ou n'ayant pas de statistiques")
    else:
        return statistiques


# Endpoint GET /joueur_connecte/valeur_portefeuille
@router.get("/valeur_portefeuille", response_model=int)
def portefeuille_joueur(pseudo: str):
    """
    Endpoint de récupération de la valeur de son portefeuille par un joueur.
    """

    valeur = JoueurDao().valeur_portefeuille(pseudo)
    
    if valeur is not None:
        return valeur
    else:
        raise HTTPException(status_code=401, detail="Pseudo inconnu")


# Endpoint GET /joueur_connecte/voir_classement
@router.get("/voir_classement", response_model=list[dict])
def voir_classement_joueur():
    """
    Endpoint permettant à un joueur de voir le classement.
    """
    classement_raw = JoueurDao().classement_par_portefeuille(limit=None)
    classement = [dict(row) for row in classement_raw]
    return classement

# Endpoint POST /joueur_connecte/rejoindre_table
@router.post("/rejoindre_table", response_model=TableRejointe)
def rejoindre_table_joueur(pseudo: str, id_table: int):
    """
    Endpoint permettant à un joueur de rejoindre une table.
    """
    succes_action, etat, message_action = tables_service.rejoindre_table(pseudo, id_table)
    reponse = TableRejointe(
        succes=succes_action,
        message=message_action
    )
    return reponse

# Endpoint GET /joueur_connecte/voir_table
@router.get("/voir_table", response_model=TableSortie)
def voir_table(id_table: int):
    """
    Endpoint pour voir une table (ses joueurs ...).
    """
    table = tables_service.get_table(id_table)
    table_sortie = TableSortie(
        id = table.id,
        nombre_joueurs = len(table.joueurs),
        blind = table.blind,
        pot = table.pot,
        indice_dealer = table.indice_dealer,
    )
    return table_sortie

# Endpoint GET /joueur_connecte/voir_tables
@router.get("/voir_tables", response_model=list[dict])
def voir_tables():
    """
    Renvoie la liste de toutes les tables avec leur nombre de joueurs et blind
    """
    etat = []
    for table in tables_service.lister_tables():
        etat.append({
            "id": table["id"],
            "nb_joueurs": table["nb_joueurs"],
            "blind": table["blind"]
        })
    return etat

# Endpoint POST /joueur_connecte/deconnexion
@router.post("/deconnexion", status_code=status.HTTP_204_NO_CONTENT)
def deconnexion(pseudo: str):
    """
    Déconnecte un joueur en mettant à jour son état dans la base.
    """
    JoueurService().se_deconnecter(pseudo)
    return  # 204 No Content