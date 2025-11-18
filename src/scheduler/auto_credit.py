from apscheduler.schedulers.background import BackgroundScheduler

from src.service.joueur_service import JoueurService

def lancer_auto_credit():
    """
    Fonction qui automatise le rechargement des portefeuilles de façon régulière.
    """
    scheduler = BackgroundScheduler()
    JoueurService().credit_auto()
    scheduler.add_job(JoueurService().credit_auto, "cron", hour=3, minute=0)
    scheduler.start()
    