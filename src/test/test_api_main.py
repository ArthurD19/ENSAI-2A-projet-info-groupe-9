from fastapi.testclient import TestClient
from src.api.api_main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur Tapis!"}


def test_routes_exist():
    """Vérifie que les routes principales existent"""
    paths = [route.path for route in app.routes]
    assert "/" in paths
    # Vérifie au moins un endpoint lié aux joueurs
    assert any("joueur" in p for p in paths)
