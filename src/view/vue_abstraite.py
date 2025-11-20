import logging

from abc import ABC, abstractmethod
from src.utils.log_decorator import log


class VueAbstraite(ABC):
    """Modèle de Vue"""

    @log
    def __init__(self, message=""):
        self.message = message
        logging.info(type(self).__name__)

    @log
    def nettoyer_console(self):
        """Insérer des lignes vides pour simuler un nettoyage"""
        for _ in range(30):
            print("")

    @log
    def afficher(self) -> None:
        """Echappe un grand espace dans le terminal pour simuler
        le changement de page de l'application"""
        self.nettoyer_console()
        # n'affiche le message que s'il s'agit d'une chaîne non vide
        if isinstance(self.message, str) and self.message.strip():
            print(self.message)
            print()

    @log
    @abstractmethod
    def choisir_menu(self):
        """Choix du menu suivant de l'utilisateur"""
        pass
