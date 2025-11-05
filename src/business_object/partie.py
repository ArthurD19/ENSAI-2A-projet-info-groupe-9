import random
from business_object.cartes import Carte
from business_object.joueurs import Joueur
from business_object.distrib import Distrib
from business_object.comptage import Comptage
from business_object.evaluateur import EvaluateurMain

class Partie:
    """Gestion complète d'une partie de poker Texas Hold'em."""

    def __init__(self, id: int, table): 
        self.id = id
        self.table = table
        self.distrib = Distrib(self.table.joueurs)
        self.comptage = Comptage()
        self.tour_actuel = "preflop"
        self.mise_max = 0
        self.indice_joueur_courant = 0

    def initialiser_blinds(self):
        """Place automatiquement la petite et la grosse blind."""
        if len(self.table.joueurs) < 2:
            return
        petite_blind = 10
        grosse_blind = 20
        joueur_pb = self.table.joueurs[self.table.indice_dealer % len(self.table.joueurs)]
        joueur_pb.miser(petite_blind)
        print(f"{joueur_pb.pseudo} place la petite blind ({petite_blind})")
        joueur_gb = self.table.joueurs[(self.table.indice_dealer + 1) % len(self.table.joueurs)]
        joueur_gb.miser(grosse_blind)
        print(f"{joueur_gb.pseudo} place la grosse blind ({grosse_blind})")
        self.mise_max = grosse_blind
        self.indice_joueur_courant = (self.table.indice_dealer + 2) % len(self.table.joueurs)

    def demarrer_partie(self):
        """Déroule un tour complet de la partie."""
        if not self.table.joueurs:
            print("Aucun joueur à la table.")
            return

        print(f"=== Début de la partie {self.id} ===")
        self.table.reset_table()
        self.distrib.deck = self.table.deck
        self.distrib.distribuer_mains()
        self.initialiser_blinds()
        self.tour_actuel = "preflop"

        while self.tour_actuel != "fin":
            print(f"\nTour actuel : {self.tour_actuel}")
            self.afficher_etat()
            self.actions_joueurs()
            self.passer_tour()

        self.annoncer_resultats()

        # Demander si les joueurs veulent rejouer
        for j in self.table.joueurs[:]:
            if j.solde > 0:
                reponse = input(f"{j.pseudo}, voulez-vous rejouer ? (oui/non) : ")
                if reponse.lower() != "oui":
                    self.table.supprimer_joueur(j)
            else:
                print(f"{j.pseudo} n'a plus d'argent et est retiré de la table.")
                self.table.supprimer_joueur(j)

        if len(self.table.joueurs) < 2:
            print("Pas assez de joueurs pour continuer. La simulation s'arrête.")
            return False
        return True

    def afficher_etat(self):
        """Affiche l'état complet de la partie."""
        print("Joueurs à la table :")
        for j in self.table.joueurs:
            etat = "En partie" if j.actif else "Couché"
            print(f"  {j.pseudo}: solde={j.solde}, mise={j.mise}, état={etat}")
        print(f"Pot principal : {self.comptage.pot}")
        print("Pots secondaires :")
        for j, montant in self.comptage.pots_perso.items():
            print(f"  {j.pseudo}: {montant}")
        print(f"Cartes sur le board : {self.table.board}")
        print(f"Taille du deck : {len(self.table.deck)}")

    def actions_joueurs(self):
        """Boucle d'enchères : tous les joueurs suivent la mise max ou se couchent."""
        nb_joueurs = len(self.table.joueurs)
        joueurs_actifs = [j for j in self.table.joueurs if j.actif]
        joueurs_a_jouer = set(joueurs_actifs)

        while len(joueurs_actifs) > 1 and joueurs_a_jouer:
            joueur = self.table.joueurs[self.indice_joueur_courant]

            if not joueur.actif or joueur.solde == 0:
                if joueur.solde == 0:
                    print(f"{joueur.pseudo} n'a plus d'argent et ne peut plus agir ce tour.")
                self.indice_joueur_courant = (self.indice_joueur_courant + 1) % nb_joueurs
                continue

            if joueur.mise == self.mise_max and joueur not in joueurs_a_jouer:
                self.indice_joueur_courant = (self.indice_joueur_courant + 1) % nb_joueurs
                continue

            print(f"\nTour de {joueur.pseudo}, solde : {joueur.solde}, mise actuelle : {joueur.mise}")
            print(f"Main : {joueur.main}")

            action = input("Que voulez-vous faire ? (miser/suivre/se coucher/voir partie) : ").lower()

            if action == "voir partie":
                self.afficher_etat()
                continue
            elif action == "miser":
                montant = int(input("Montant à miser (ajouté à votre mise actuelle) : "))
                total = joueur.mise + montant
                if total <= self.mise_max:
                    print("Vous devez relancer au-dessus de la mise actuelle.")
                    continue
                joueur.miser(montant)
                self.mise_max = joueur.mise
                joueurs_a_jouer = {j for j in joueurs_actifs if j != joueur}
            elif action == "suivre":
                montant_a_ajouter = self.mise_max - joueur.mise
                if montant_a_ajouter > 0:
                    joueur.suivre(self.mise_max)
            elif action == "se coucher":
                joueur.se_coucher()
                joueurs_actifs.remove(joueur)
                if joueur in joueurs_a_jouer:
                    joueurs_a_jouer.remove(joueur)
            else:
                print("Action non reconnue.")
                continue

            if joueur in joueurs_a_jouer:
                joueurs_a_jouer.remove(joueur)

            self.indice_joueur_courant = (self.indice_joueur_courant + 1) % nb_joueurs

        # Si un seul joueur reste actif → il gagne immédiatement
        if len(joueurs_actifs) == 1:
            gagnant = joueurs_actifs[0]
            for j in self.table.joueurs:
                if j.mise > 0:
                    self.comptage.ajouter_pot_perso(j, j.mise)
                    j.mise = 0
            self.comptage.ajouter_pot()
            print(f"{gagnant.pseudo} remporte le pot principal ({self.comptage.pot}) avec la meilleure main !")
            gagnant.solde += self.comptage.pot
            self.comptage.pot = 0
            self.tour_actuel = "fin"

    def passer_tour(self):
        """Fait avancer la partie au tour suivant et ajoute les mises au pot."""
        for j in self.table.joueurs:
            if j.mise > 0:
                self.comptage.ajouter_pot_perso(j, j.mise)
                j.mise = 0
        self.comptage.ajouter_pot()
        self.mise_max = 0

        if self.tour_actuel == "preflop":
            self.distrib.distribuer_flop()
            self.table.board = self.distrib.flop
            self.tour_actuel = "flop"
        elif self.tour_actuel == "flop":
            self.distrib.distribuer_turn()
            self.table.board.append(self.distrib.turn)
            self.tour_actuel = "turn"
        elif self.tour_actuel == "turn":
            self.distrib.distribuer_river()
            self.table.board.append(self.distrib.river)
            self.tour_actuel = "river"
        elif self.tour_actuel == "river":
            self.tour_actuel = "fin"
            print("Fin de la main.")

    def annoncer_resultats(self):
        """Évalue et annonce la combinaison de chaque joueur et le(s) gagnant(s)."""
        joueurs_en_jeu = [j for j in self.table.joueurs if j.actif and j.solde > 0]
        if not joueurs_en_jeu:
            print("Aucun joueur n'est en jeu.")
            return

        # Évaluation des mains
        scores = {}
        for j in joueurs_en_jeu:
            cartes_totales = j.main + self.table.board
            evaluateur = EvaluateurMain(cartes_totales)
            resultat = evaluateur.evalue_main()
            scores[j] = resultat
            # Affichage compatible avec le nouvel EvaluateurMain
            tiebreaker_str = [v.name for v in resultat.tiebreaker_cards]
            print(f"{j.pseudo} a {resultat.combinaison.name} avec kickers {tiebreaker_str}")

        # Trouver le(s) gagnant(s)
        gagnants = [joueurs_en_jeu[0]]
        for j in joueurs_en_jeu[1:]:
            cmp = EvaluateurMain.comparer_mains(scores[j], scores[gagnants[0]])
            if cmp == 1:
                gagnants = [j]  # nouveau gagnant
            elif cmp == 0:
                gagnants.append(j)  # égalité

        # Distribuer le pot équitablement
        if self.comptage.pot > 0:
            part = self.comptage.pot // len(gagnants)
            for j in gagnants:
                j.solde += part
            print(f"Gagnant(s) : {', '.join(j.pseudo for j in gagnants)} remporte(nt) {part} chacun !")

        # Reset du pot
        self.comptage.pot = 0
        self.comptage.pots_perso = {}
