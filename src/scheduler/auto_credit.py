from apscheduler.schedulers.background import BackgroundScheduler

from src.service.joueur_service import JoueurService
import pytz

def lancer_auto_credit():
    """
    Fonction qui automatise le rechargement des portefeuilles de façon régulière.
    """
    scheduler = BackgroundScheduler(timezone=pytz.timezone("Europe/Paris"))
    JoueurService().credit_auto()
    scheduler.add_job(JoueurService().credit_auto, "cron", hour=15, minute=30)
    scheduler.start()
