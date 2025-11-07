import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.joueur_router import router as joueur_router
from src.api.joueur_connecte_router import router as joueur_connecte_router
from src.api.joueur_en_jeu_router import router as joueur_en_jeu_router

# Création de l'application FastAPI
app = FastAPI(
    title="API Joueurs",
    description="API pour la gestion des joueurs, connexion, inscription, stats et portefeuille",
    version="1.0.0",
    root_path="/proxy/8000"
)

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
    return {"message": "API Joueurs en ligne"}
