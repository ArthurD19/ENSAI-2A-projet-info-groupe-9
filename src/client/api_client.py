# src/client/api_client.py
import os
import requests

BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")
TIMEOUT = 5  # secondes

class APIError(Exception):
    pass

def _url(path: str) -> str:
    # path doit commencer par '/'
    return BASE_URL.rstrip("/") + path

def post(path: str, params=None, json=None):
    try:
        r = requests.post(_url(path), params=params, json=json, timeout=TIMEOUT)
        r.raise_for_status()
        # On renvoie le json si possible sinon le texte
        try:
            return r.json()
        except ValueError:
            return r.text
    except requests.HTTPError as e:
        # Propagation d'une exception avec message utile
        raise APIError(f"HTTP {r.status_code}: {r.text}") from e
    except Exception as e:
        raise APIError(str(e)) from e

def get(path: str, params=None):
    try:
        r = requests.get(_url(path), params=params, timeout=TIMEOUT)
        r.raise_for_status()
        try:
            return r.json()
        except ValueError:
            return r.text
    except requests.HTTPError as e:
        raise APIError(f"HTTP {r.status_code}: {r.text}") from e
    except Exception as e:
        raise APIError(str(e)) from e
