from fastapi import FastAPI
from src.api.joueur_router import router

app = FastAPI()
app.include_router(router)
