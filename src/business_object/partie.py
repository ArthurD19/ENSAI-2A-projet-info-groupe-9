import random
from business_object.cartes import Carte
from business_object.joueurs import Joueur
from business_object.distrib import Distrib
from business_object.comptage import Comptage
from business_object.evaluateur import EvaluateurMain
from dao.statistique_dao import StatistiqueDao


class Partie:
    """Gestion complète d'une partie de poker Texas Hold'em."""

    GROSSE_BLIND = 20  # constante globale pour la grosse blind

    def __init__(self, id: int, table): 
        self.id = id
        self.table = table
        self.distrib = Distrib(self.table.joueurs)
        self.comptage = Comptage()
        self.tour_actuel = "preflop"
        self.mise_max = 0
        self.indice_joueur_courant = 0
        self.stats_dao = StatistiqueDao() 

    def initialiser_blinds(self):
        nb_joueurs = len(self.table.joueurs)
        if nb_joueurs < 2:
            print("Pas assez de joueurs pour initialiser les blinds.")
            return

        petite_blind = 10
        grosse_blind = Partie.GROSSE_BLIND

        dealer_idx = self.table.indice_dealer % nb_joueurs
        dealer = self.table.joueurs[dealer_idx]
        print(f"Dealer : {dealer.pseudo}")

        pb_idx = (dealer_idx + 1) % nb_joueurs
        joueur_pb = self.table.joueurs[pb_idx]
        joueur_pb.miser(petite_blind)
        print(f"{joueur_pb.pseudo} place la petite blind ({petite_blind})")

        gb_idx = (pb_idx + 1) % nb_joueurs
        joueur_gb = self.table.joueurs[gb_idx]
        joueur_gb.miser(grosse_blind)
        print(f"{joueur_gb.pseudo} place la grosse blind ({grosse_blind})")

        self.indice_joueur_courant = (gb_idx + 1) % nb_joueurs
        joueur_courant = self.table.joueurs[self.indice_joueur_courant]
        print(f"Premier joueur à agir : {joueur_courant.pseudo}")

        self.mise_max = grosse_blind
        self.table.indice_dealer = (self.table.indice_dealer + 1) % nb_joueurs

    def demarrer_partie(self):
        if not self.table.joueurs:
            print("Aucun joueur à la table.")
            return

        continuer = True
        while continuer:
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
            # gestion_rejouer retourne True si on continue, False si la partie doit s'arrêter
            continuer = self.gestion_rejouer()

    def afficher_etat(self):
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
        nb_joueurs = len(self.table.joueurs)
        joueurs_actifs = [j for j in self.table.joueurs if j.actif]
        joueurs_a_jouer = set(joueurs_actifs)
        grosse_blind = Partie.GROSSE_BLIND

        while len(joueurs_actifs) > 1 and joueurs_a_jouer:
            # Filtrer les joueurs qui ne peuvent plus jouer (ALL-IN ou couchés)
            joueurs_a_jouer = {j for j in joueurs_a_jouer if j.actif and j.solde > 0}

            # Vérifier si la partie peut se terminer
            if len(joueurs_actifs) <= 1 or not joueurs_a_jouer:
                break

            # Puis le reste du code pour choisir le joueur courant et demander l'action
            joueur = self.table.joueurs[self.indice_joueur_courant]

            # Si le joueur est inactif ou n'a plus de solde
            if not joueur.actif or joueur.solde == 0:
                self.indice_joueur_courant = (self.indice_joueur_courant + 1) % nb_joueurs
                continue

            # Si le joueur a déjà égalé la mise et n'a plus rien à faire
            if joueur.mise == self.mise_max and joueur not in joueurs_a_jouer:
                self.indice_joueur_courant = (self.indice_joueur_courant + 1) % nb_joueurs
                continue

            print(f"\nTour de {joueur.pseudo}, solde : {joueur.solde}, mise actuelle : {joueur.mise}")
            print(f"Main : {joueur.main}")

            action = input("Que voulez-vous faire ? (miser/suivre/se coucher/all-in/voir partie) : ").lower()

            if action == "voir partie":
                self.afficher_etat()
                continue

            elif action == "miser":
                try:
                    montant = int(input("Montant à miser (ajouté à votre mise actuelle) : "))
                except ValueError:
                    print("Erreur : vous devez entrer un entier pour la mise.")
                    continue

                if montant <= 0:
                    print("Vous devez miser un montant positif.")
                    continue
                if montant < grosse_blind:
                    print(f"Vous ne pouvez pas miser moins que la grosse blind ({grosse_blind}).")
                    continue
                elif montant > grosse_blind and montant < 2 * grosse_blind:
                    print(f"Vous devez miser soit exactement la grosse blind ({grosse_blind}), soit au moins {2*grosse_blind}.")
                    continue

                if montant + joueur.mise <= self.mise_max:
                    print("Vous devez relancer au-dessus de la mise actuelle.")
                    continue
                if montant > joueur.solde:
                    print("Vous ne pouvez pas miser plus que votre solde.")
                    continue

                joueur.miser(montant)
                self.mise_max = joueur.mise
                joueurs_a_jouer = {j for j in joueurs_actifs if j != joueur}
                self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_mises")

            elif action == "suivre":
                montant_a_ajouter = self.mise_max - joueur.mise
                if montant_a_ajouter <= 0:
                    print("Vous avez déjà égalé la mise.")
                elif montant_a_ajouter >= joueur.solde:
                    reponse = input(
                        f"Suivre nécessite {montant_a_ajouter}, mais il vous reste {joueur.solde}. Voulez-vous faire ALL-IN ? (oui/non) : "
                    )
                    if reponse.lower() == "oui":
                        joueur.miser(joueur.solde)
                        print(f"{joueur.pseudo} fait ALL-IN avec {joueur.mise} !")
                    else: continue
                else:
                    joueur.suivre(self.mise_max)
                self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_suivis")

            elif action == "all-in":
                joueur.miser(joueur.solde)
                self.mise_max = max(self.mise_max, joueur.mise)
                print(f"{joueur.pseudo} fait ALL-IN avec {joueur.mise} !")
                joueurs_a_jouer = {j for j in joueurs_actifs if j != joueur}

            elif action == "se coucher":
                if joueur.solde == 0:
                    print("Vous êtes ALL-IN, vous ne pouvez plus vous coucher, vous ne pouvez que suivre/all-in.")
                else:
                    joueur.se_coucher()
                    joueurs_actifs.remove(joueur)
                    if joueur in joueurs_a_jouer:
                        joueurs_a_jouer.remove(joueur)
                    self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_folds")

            else:
                print("Action non reconnue.")
                continue

            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_total_mains_jouees")
            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_mains_jouees_session")

            if joueur in joueurs_a_jouer:
                joueurs_a_jouer.remove(joueur)

            self.indice_joueur_courant = (self.indice_joueur_courant + 1) % nb_joueurs

        # Si un seul joueur reste actif
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
        # Joueurs encore "en jeu" (actifs et avec solde > 0)
        joueurs_en_jeu = [j for j in self.table.joueurs if j.actif or j.mise > 0]

        # Si tous les joueurs sont ALL-IN et n'ont plus de solde, on prend ceux qui ont misé
        if not joueurs_en_jeu:
            joueurs_en_jeu = [j for j in self.table.joueurs if j.actif or j.mise > 0]

        
        if len(joueurs_en_jeu) <= 1:
            gagnant = joueurs_en_jeu[0]
            gagnant.solde += self.comptage.pot
            print(f"{gagnant.pseudo} remporte le pot principal ({self.comptage.pot}) !")
            self.comptage.pot = 0
            return
        

        scores = {}
        for j in joueurs_en_jeu:
            cartes_totales = j.main + self.table.board
            evaluateur = EvaluateurMain(cartes_totales)
            resultat = evaluateur.evalue_main()
            scores[j] = resultat
            tiebreaker_str = [v.name for v in resultat.tiebreaker_cards]
            print(f"{j.pseudo} a {resultat.combinaison.name} avec kickers {tiebreaker_str}")

        gagnants = [joueurs_en_jeu[0]]
        for j in joueurs_en_jeu[1:]:
            cmp = EvaluateurMain.comparer_mains(scores[j], scores[gagnants[0]])
            if cmp == 1:
                gagnants = [j]
            elif cmp == 0:
                gagnants.append(j)

        if self.comptage.pot > 0:
            part = self.comptage.pot // len(gagnants)
            for j in gagnants:
                j.solde += part
            if len(gagnants) == 1:
                print(f"{gagnants[0].pseudo} remporte le pot principal ({part}) !")
            else:
                print(f"Gagnants : {', '.join(j.pseudo for j in gagnants)} remportent {part} chacun !")

        self.comptage.pot = 0
        self.comptage.pots_perso = {}


    def gestion_rejouer(self):
        """Demande aux joueurs s'ils veulent rejouer ou quitter la table."""
        print("\n=== Portefeuille des joueurs avant la prochaine main ===")
        for j in self.table.joueurs:
            print(f"{j.pseudo} : solde = {j.solde}")

        for j in self.table.joueurs[:]:
            if j.solde >= 20:
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
