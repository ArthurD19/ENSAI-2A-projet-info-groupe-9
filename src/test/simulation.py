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
