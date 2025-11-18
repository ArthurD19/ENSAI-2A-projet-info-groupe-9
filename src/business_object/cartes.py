import random
from enum import Enum


class couleurs(Enum):
    COEUR = "Coeur"
    PIQUE = "Pique"
    CARREAU = "Carreau"
    TREFLE = "Trèfle"


class valeurs(Enum):
    DEUX = "2"
    TROIS = "3"
    QUATRE = "4"
    CINQ = "5"
    SIX = "6"
    SEPT = "7"
    HUIT = "8"
    NEUF = "9"
    DIX = "10"
    VALET = "Valet"
    DAME = "Dame"
    ROI = "Roi"
    AS = "As"


class combinaisons(Enum):
    HAUTEUR = 1
    PAIRE = 2
    DOUBLE_PAIRE = 3
    BRELAN = 4
    QUINTE = 5
    COULEUR = 6
    FULL = 7
    CARRE = 8
    QUINTE_FLUSH = 9
    QUINTE_FLUSH_ROYALE = 10


class Carte:
    def __init__(self, couleur: str, valeur: str)-> None:
        self.couleur = couleur
        self.valeur = valeur

    def __str__(self)->str:
        return f"{self.valeur.value} de {self.couleur.value}"

    def __repr__(self)->str:
        return f"Carte({self.valeur.value}, {self.couleur.value})"


class Deck:
    def __init__(self)->None:
        self.cartes = []

    def remplir(self)->None:
        """ rempli un deck avec toutes les cartes"""
        self.cartes = [
            Carte(couleur, valeur) for couleur in couleurs for valeur in valeurs
            ]

    def melanger(self)->None:
        """ mélange le deck"""
        random.shuffle(self.cartes)

    def tirer(self)->Carte:
        """tire une carte du deck"""
        if len(self.cartes) < 1:
            raise ValueError("Pas assez de cartes dans le deck.")
        return self.cartes.pop()

    def ajouter(self, carte: Carte)->None:
        "ajoute une carte dans le deck"
        self.cartes.append(carte)

    def __len__(self)->int:
        return len(self.cartes)
