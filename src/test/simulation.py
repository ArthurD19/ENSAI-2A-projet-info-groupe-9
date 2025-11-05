from business_object.cartes import Carte, Deck
from business_object.joueurs import Joueur
from business_object.table import Table
from business_object.partie import Partie
from dao.statistique_dao import StatistiqueDao

# Création de l'objet StatistiqueDao
stats_dao = StatistiqueDao()

# Création des joueurs
alice = Joueur("Alice", 1000)
bob = Joueur("Bob", 1000)
charlie = Joueur("Charlie", 1000)

# Créer les statistiques pour ces joueurs s'ils n'existent pas
for j in [alice, bob, charlie]:
    stats_dao.creer_statistiques_pour_joueur(j.pseudo)

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
    
    continuer_simulation = partie.demarrer_partie()
    partie_numero += 1

# Après la simulation, afficher les stats mises à jour
for joueur in table.joueurs:
    stats = stats_dao.trouver_statistiques_par_id(joueur.pseudo)
    print(f"\nStatistiques de {joueur.pseudo}:")
    for k, v in stats.items():
        print(f"  {k} : {v}")

print("Simulation terminée : pas assez de joueurs pour continuer.")
