from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.joueur_router import router as joueur_router
from src.api.joueur_connecte_router import router as joueur_connecte_router
from src.api.joueur_en_jeu_router import router as joueur_en_jeu_router
from src.api.var_utiles import tables_service
from src.scheduler.auto_credit import lancer_auto_credit


# Création de l'application FastAPI
app = FastAPI(
    title="TAPIS!",
    description="API pour le serveur de poker",
    version="1.0.0",
    root_path="/proxy/8000"
)


@app.on_event("startup")
def init_tables_et_parties():
    """
    Initialisation des tables et parties à l'ouverture du serveur.
    """
    global tables
    print("Initialisation des tables et parties...")

    for id_table, partie in tables_service.parties.items():
        print(f"Table {id_table} créée avec partie associée: {partie is not None}")


@app.on_event("startup")
def demarrer_scheduler():
    """
    Initialisation du rechargement automatique à l'ouverture du serveur.
    """
    global scheduler
    print("[SCHEDULER] Démarrage du créditage automatique")
    scheduler = lancer_auto_credit()


@app.on_event("shutdown")
def arreter_scheduler():
    """
    Arrêt du rechargement automatique à la fermeture du serveur.
    """
    global scheduler
    if scheduler:
        print("[SCHEDULER] Arrêt du scheduler")
        scheduler.shutdown()


# Middleware CORS si tu comptes faire des requêtes depuis un front
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Ajouter ici les URLs autorisées pour ton frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion du router joueur
app.include_router(joueur_router)
app.include_router(joueur_connecte_router)
app.include_router(joueur_en_jeu_router)


# Endpoint racine pour tester si le serveur fonctionne
@app.get("/")
def root():
    return {"message": "Bienvenue sur Tapis!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api_main:app",
        host="0.0.0.0",   # indispensable pour Onyxia
        port=8000,        # port exposé et forwardé
        reload=True       # uniquement en dev
    )
