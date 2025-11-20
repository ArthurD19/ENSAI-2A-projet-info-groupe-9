
from business_object.joueurs import Joueur
from business_object.table import Table
from business_object.partie import Partie
from service.partie_service import PartieService

# --- Création des joueurs ---
alice = Joueur("Alice", 100)
bob = Joueur("Bob", 100)
charlie = Joueur("Charlie", 100)

# --- Création de la table ---
table = Table(id=1, blind=10)
table.ajouter_joueur(alice)
table.ajouter_joueur(bob)
table.ajouter_joueur(charlie)

# --- Création de la partie et du service ---
partie = Partie(id=1, table=table)
service = PartieService(partie)

# --- Initialisation des blinds ---
partie.initialiser_blinds()

def afficher_etat(etat):
    print(f"Tour: {etat.tour_actuel}, Pot: {etat.pot}, Joueur courant: {etat.joueur_courant}")
    print("Joueurs:")
    for j in etat.joueurs:
        print(f"  {j['pseudo']} - Solde: {j['solde']}, Mise: {j['mise']}, Actif: {j['actif']}")
    print(f"Board: {[str(c) for c in etat.board]}")
    print("---")

# --- Préflop : tous suivent ---
for pseudo in ["Alice", "Bob", "Charlie"]:
    success, etat, msg = service.suivre(pseudo)
    print(f"{pseudo} suit -> {msg}")
    afficher_etat(etat)

# --- Flop : Bob mise 20, les autres suivent ---
partie.passer_tour()  # On distribue le flop
print("\n--- Flop distribué ---")
afficher_etat(partie.etat)

success, etat, msg = service.miser("Bob", 20)
print(f"Bob mise 20 -> {msg}")
afficher_etat(etat)

success, etat, msg = service.suivre("Alice")
print(f"Alice suit -> {msg}")
afficher_etat(etat)

success, etat, msg = service.suivre("Charlie")
print(f"Charlie suit -> {msg}")
afficher_etat(etat)

# --- Turn : tous suivent ---
partie.passer_tour()  # Turn distribué
print("\n--- Turn distribué ---")
afficher_etat(partie.etat)

for pseudo in ["Alice", "Bob", "Charlie"]:
    success, etat, msg = service.suivre(pseudo)
    print(f"{pseudo} suit -> {msg}")
    afficher_etat(etat)

# --- River : Alice se couche, Bob mise 30, Charlie suit ---
partie.passer_tour()  # River distribué
print("\n--- River distribué ---")
afficher_etat(partie.etat)

success, etat, msg = service.se_coucher("Alice")
print(f"Alice se couche -> {msg}")
afficher_etat(etat)

success, etat, msg = service.miser("Bob", 30)
print(f"Bob mise 30 -> {msg}")
afficher_etat(etat)

success, etat, msg = service.suivre("Charlie")
print(f"Charlie suit -> {msg}")
afficher_etat(etat)

# --- Affichage des résultats finaux ---
print("\n--- Résultats de la partie ---")
for resultat in etat.resultats:
    print(f"{resultat['pseudo']} gagne : {resultat.get('description','')}")

# --- Solde final des joueurs ---
print("\n--- Solde final des joueurs ---")
for j in partie.table.joueurs:
    print(f"{j.pseudo}: {j.solde} jetons")
"""

# fichier : test_rejoindre_table_terminal.py

from service.table_service import TableService
from dao.joueur_dao import JoueurDao

# Simuler la DAO pour donner un solde fixe à tous les joueurs
JoueurDao().valeur_portefeuille = lambda pseudo: 100

# Initialisation du service avec 1 table
service = TableService(nb_tables=1, blind=20)

# Joueurs à ajouter
pseudos = ["lucas", "marie", "alice"]

for pseudo in pseudos:
    success, etat, msg = service.rejoindre_table(pseudo, 1)
    print(f"\nJoueur '{pseudo}' rejoint la table : {success}, message : {msg}")

    # Affichage de l'état de la table
    table = service.get_table(1)
    print("Joueurs à la table :")
    for j in table.joueurs:
        print(f" - {j.pseudo}, solde: {j.solde}, actif: {j.actif}, mise: {j.mise}")

    # Affichage de l'état de la partie
    partie = service.parties[1]
    print("État de la partie :")
    print(f" - Partie terminée ? {etat.finie}")
    print(f" - Pot actuel : {etat.pot}")
    print(f" - Joueurs actifs dans la partie : {[j.pseudo for j in partie.table.joueurs if j.actif]}")
    print(f" - Liste d'attente : {[j['pseudo'] for j in etat.liste_attente]}")
"""