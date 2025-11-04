from business_object.cartes import Carte, Deck
from business_object.joueurs import Joueur
from business_object.table import Table
from business_object.partie import Partie

# Création des joueurs
alice = Joueur("Alice", 1000)
bob = Joueur("Bob", 1000)
charlie = Joueur("Charlie", 1000)

# Création de la table et ajout des joueurs
table = Table(1)
table.ajouter_joueur(alice)
table.ajouter_joueur(bob)
table.ajouter_joueur(charlie)

# Création de la partie
partie_numero = 1
continuer_simulation = True

while continuer_simulation and len(table.joueurs) >= 2:
    partie = Partie(partie_numero, table)
    # Lance la partie/tour et récupère si on peut continuer
    continuer_simulation = partie.demarrer_partie()  # <- ici on appelle la bonne méthode
    partie_numero += 1

print("Simulation terminée : pas assez de joueurs pour continuer.")
