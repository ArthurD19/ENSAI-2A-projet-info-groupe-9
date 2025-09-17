import json
import os
from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
from typing import Optional

# ==========================
# ======= Config ===========
# ==========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(BASE_DIR, "data", "data.json")

app = FastAPI(
    title="TAPIS!",
    root_path="/proxy/8000"  
)

# ==========================
# ======= Modèles ==========
# ==========================
class SignupIn(BaseModel):
    pseudo: str
    password: str
    code_parrainage: Optional[str] = None


class LoginIn(BaseModel):
    pseudo: str
    password: str


class Joueur(BaseModel):
    pseudo: str
    solde: float = 100.0
    wins: int = 0
    losses: int = 0
    gains: float = 0.0


# ==========================
# ======= Utils JSON =======
# ==========================
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ==========================
# ======= Gérer compte =====
# ==========================
@app.post("/joueur/gerer_compte/creer_compte", tags=["Joueur - Gérer compte"])
def creer_compte(data: SignupIn):
    db = load_data()
    if data.pseudo in db["joueurs"]:
        raise HTTPException(status_code=400, detail="Pseudo déjà utilisé")

    db["joueurs"][data.pseudo] = {
        "pseudo": data.pseudo,
        "password": data.password,
        "solde": 100.0,
        "wins": 0,
        "losses": 0,
        "gains": 0.0,
    }

    save_data(db)
    return {"message": "Compte créé", "pseudo": data.pseudo}


@app.post("/joueur/gerer_compte/se_connecter", tags=["Joueur - Gérer compte"])
def se_connecter(data: LoginIn):
    db = load_data()
    joueur = db["joueurs"].get(data.pseudo)
    if not joueur or joueur["password"] != data.password:
        raise HTTPException(status_code=400, detail="Pseudo ou mot de passe incorrect")
    return {
        "pseudo": joueur["pseudo"],
        "solde": joueur["solde"],
        "wins": joueur["wins"],
        "losses": joueur["losses"],
        "gains": joueur["gains"],
    }


# ==========================
# ======= Communauté =======
# ==========================
@app.get("/joueur/communaute/classement", tags=["Joueur - Communauté"])
def classement():
    db = load_data()
    joueurs = list(db["joueurs"].values())
    classement = sorted(joueurs, key=lambda j: j["solde"], reverse=True)
    return [{"pseudo": j["pseudo"], "solde": j["solde"]} for j in classement]


@app.get("/joueur/communaute/stat_joueur/{pseudo}", tags=["Joueur - Communauté"])
def stat_joueur(pseudo: str):
    db = load_data()
    if pseudo not in db["joueurs"]:
        raise HTTPException(status_code=404, detail="Joueur inconnu")
    j = db["joueurs"][pseudo]
    return {
        "pseudo": j["pseudo"],
        "solde": j["solde"],
        "wins": j["wins"],
        "losses": j["losses"],
        "gains": j["gains"],
    }


# ==========================
# ======= Jouer ===========
# ==========================
@app.get("/joueur/jouer/voir_tables", tags=["Joueur - Jouer"])
def voir_tables():
    db = load_data()
    return [{"table": tid, "nb_joueurs": len(players)} for tid, players in db["tables"].items()]


@app.post("/joueur/jouer/rejoindre_table/{table_id}", tags=["Joueur - Jouer"])
def rejoindre_table(table_id: str, pseudo: str = Query(..., description="Pseudo du joueur")):
    db = load_data()
    if pseudo not in db["joueurs"]:
        raise HTTPException(status_code=404, detail="Joueur inconnu")
    if table_id not in db["tables"]:
        raise HTTPException(status_code=404, detail="Table inexistante")
    if pseudo in db["tables"][table_id]:
        raise HTTPException(status_code=400, detail="Déjà à cette table")

    db["tables"][table_id].append(pseudo)
    save_data(db)
    return {"message": f"{pseudo} a rejoint la table {table_id}", "players": db["tables"][table_id]}


@app.post("/joueur/jouer/quitter_table/{table_id}", tags=["Joueur - Jouer"])
def quitter_table(table_id: str, pseudo: str = Query(..., description="Pseudo du joueur")):
    db = load_data()
    if pseudo not in db["joueurs"]:
        raise HTTPException(status_code=404, detail="Joueur inconnu")
    if table_id not in db["tables"]:
        raise HTTPException(status_code=404, detail="Table inexistante")
    if pseudo not in db["tables"][table_id]:
        raise HTTPException(status_code=400, detail="Joueur pas à cette table")

    db["tables"][table_id].remove(pseudo)
    save_data(db)
    return {"message": f"{pseudo} a quitté la table {table_id}", "players": db["tables"][table_id]}


# ==========================
# ======= Action ===========
# ==========================
@app.post("/joueur/action/check/{table_id}", tags=["Joueur - Action"])
def check(table_id: str, pseudo: str = Query(..., description="Pseudo du joueur")):
    return {"message": f"{pseudo} a fait check à la table {table_id}"}


@app.post("/joueur/action/miser/{table_id}", tags=["Joueur - Action"])
def miser(table_id: str, pseudo: str = Query(..., description="Pseudo du joueur"), montant: float = Query(..., description="Montant de la mise")):
    return {"message": f"{pseudo} a misé {montant} à la table {table_id}"}


@app.post("/joueur/action/all_in/{table_id}", tags=["Joueur - Action"])
def all_in(table_id: str, pseudo: str = Query(..., description="Pseudo du joueur")):
    return {"message": f"{pseudo} a fait all-in à la table {table_id}"}


@app.post("/joueur/action/se_coucher/{table_id}", tags=["Joueur - Action"])
def se_coucher(table_id: str, pseudo: str = Query(..., description="Pseudo du joueur")):
    return {"message": f"{pseudo} s'est couché à la table {table_id}"}


# ==========================
# ======= Admin ===========
# ==========================
@app.delete("/admin/supprimer_joueur/{pseudo}", tags=["Admin"])
def supprimer_joueur(pseudo: str = Path(..., description="Pseudo du joueur à supprimer")):
    db = load_data()
    if pseudo not in db["joueurs"]:
        raise HTTPException(status_code=404, detail="Joueur inconnu")
    db["joueurs"].pop(pseudo)
    for table_id, players in db["tables"].items():
        if pseudo in players:
            players.remove(pseudo)
    save_data(db)
    return {"message": f"Joueur {pseudo} supprimé"}


@app.get("/admin/info_joueur/{pseudo}", tags=["Admin"])
def info_joueur(pseudo: str = Path(..., description="Pseudo du joueur")):
    db = load_data()
    if pseudo not in db["joueurs"]:
        raise HTTPException(status_code=404, detail="Joueur inconnu")
    return db["joueurs"][pseudo]


@app.post("/admin/crediter_joueur/{pseudo}", tags=["Admin"])
def crediter_joueur(
    pseudo: str = Path(..., description="Pseudo du joueur"),
    montant: float = Query(..., description="Montant à créditer")
):
    db = load_data()
    if pseudo not in db["joueurs"]:
        raise HTTPException(status_code=404, detail="Joueur inconnu")
    db["joueurs"][pseudo]["solde"] += montant
    save_data(db)
    return {"message": f"{pseudo} crédité de {montant}", "solde": db["joueurs"][pseudo]["solde"]}


@app.post("/admin/penaliser_joueur/{pseudo}", tags=["Admin"])
def penaliser_joueur(
    pseudo: str = Path(..., description="Pseudo du joueur"),
    montant: float = Query(..., description="Montant à retirer")
):
    db = load_data()
    if pseudo not in db["joueurs"]:
        raise HTTPException(status_code=404, detail="Joueur inconnu")
    db["joueurs"][pseudo]["solde"] -= montant
    save_data(db)
    return {"message": f"{pseudo} pénalisé de {montant}", "solde": db["joueurs"][pseudo]["solde"]}


@app.get("/admin/lister_joueurs_table/{table_id}", tags=["Admin"])
def lister_joueurs_table(table_id: str = Path(..., description="ID de la table")):
    db = load_data()
    if table_id not in db["tables"]:
        raise HTTPException(status_code=404, detail="Table inexistante")
    return {"table": table_id, "joueurs": db["tables"][table_id]}
