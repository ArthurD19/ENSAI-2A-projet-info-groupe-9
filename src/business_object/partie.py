import random

from business_object.cartes import Carte
from business_object.joueurs import Joueur
from business_object.distrib import Distrib
from business_object.comptage import Comptage
from business_object.evaluateur import EvaluateurMain

from dao.statistique_dao import StatistiqueDao


class EtatPartie:
    def __init__(self):
        self.id_partie: int
        self.tour_actuel: str = "preflop"
        self.joueurs: list[dict] = []           # contient : pseudo, solde, mise, actif
        self.board: list[str] = []
        self.pot: int = 0
        self.pots_secondaires: dict = {}
        self.mise_max: int = 0
        self.joueur_courant: str | None = None
        self.finie: bool = True                # True si la partie est terminée
        self.resultats: list[dict] = []        # liste des gagnants avec info sur leur main et kickers
        self.rejouer: dict[str, bool | None] = {}
        self.liste_attente: list[dict] = []


class Partie:
    """Gestion complète d'une partie de poker Texas Hold'em sans input/output."""

    GROSSE_BLIND = 20

    def __init__(self, id: int, table) -> None:
        self.id = id
        self.table = table
        self.distrib = Distrib(self.table.joueurs)
        self.comptage = Comptage()
        self.tour_actuel = "preflop"
        self.mise_max = 0
        self.indice_joueur_courant = 0
        self.stats_dao = StatistiqueDao()
        self.etat = EtatPartie()
        self.etat.id_partie = id
        self.joueurs_ayant_joue: dict[str, bool] = {}

    def _mettre_a_jour_etat(self):
        self.etat.tour_actuel = self.tour_actuel
        self.etat.joueurs = [
            {"pseudo": j.pseudo, "solde": j.solde, "mise": j.mise, "actif": j.actif}
            for j in self.table.joueurs
        ]
        self.etat.board = [str(c) for c in self.table.board]
        self.etat.pot = self.comptage.pot
        self.etat.pots_secondaires = {j.pseudo: montant for j, montant in self.comptage.pots_perso.items()}
        self.etat.mise_max = self.mise_max
        if self.table.joueurs and 0 <= self.indice_joueur_courant < len(self.table.joueurs):
            self.etat.joueur_courant = self.table.joueurs[self.indice_joueur_courant].pseudo
        else:
            self.etat.joueur_courant = None

    def initialiser_blinds(self):
        nb_joueurs = len(self.table.joueurs)
        if nb_joueurs < 2:
            return  # pas assez de joueurs, on ne fait rien

        self.distrib.distribuer_mains()

        grosse_blind = Partie.GROSSE_BLIND
        petite_blind = grosse_blind // 2

        dealer_idx = self.table.indice_dealer % nb_joueurs
        pb_idx = (dealer_idx + 1) % nb_joueurs
        gb_idx = (pb_idx + 1) % nb_joueurs

        self.table.joueurs[pb_idx].miser(petite_blind)
        self.table.joueurs[gb_idx].miser(grosse_blind)

        self.mise_max = grosse_blind
        self.indice_joueur_courant = (gb_idx + 1) % nb_joueurs
        self.table.indice_dealer = (self.table.indice_dealer + 1) % nb_joueurs

        self._mettre_a_jour_etat()

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
            self.annoncer_resultats()

        self.joueurs_ayant_joue = {j.pseudo: False for j in self.table.joueurs if j.actif}
        
        self._mettre_a_jour_etat()

    def actions_joueur(self, pseudo: str, action: str, montant: int | None = None):
        joueur = next((j for j in self.table.joueurs if j.pseudo == pseudo), None)
        if not joueur or not joueur.actif:
            return self.etat

        self.joueurs_ayant_joue[joueur.pseudo] = True

        if action == "miser" and montant is not None:
            joueur.miser(montant)
            self.mise_max = joueur.mise
            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_mises")

        elif action == "suivre":
            joueur.suivre(self.mise_max)
            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_suivis")

        elif action == "all-in":
            joueur.miser(joueur.solde)
            self.mise_max = max(self.mise_max, joueur.mise)
            # suppression de la stat "nombre_allin" pour les tests

        elif action == "se_coucher":
            joueur.se_coucher()
            self.comptage.pot += joueur.mise
            joueur.mise = 0
            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_folds")
            actifs = [j for j in self.table.joueurs if j.actif]
            if len(actifs) == 1:
                self.indice_joueur_courant = self.table.joueurs.index(actifs[0])
                self.annoncer_resultats()

        self._mettre_a_jour_etat()

        if self._tour_termine():
            self.passer_tour()
            self._mettre_a_jour_etat()

        return self.etat
    
    def _tour_termine(self) -> bool:
        """
        Vérifie si tous les joueurs actifs ont misé la même somme,
        ou s'il ne reste qu'un seul joueur actif.
        """
        actifs = [j for j in self.table.joueurs if j.actif]
        if len(actifs) <= 1:
            return True

        mises_actifs = [j.mise for j in actifs]
        mises_equivalentes = len(set(mises_actifs)) == 1

        # Vérifie que tous les joueurs actifs ont joué au moins une fois
        tous_ont_joue = all(self.joueurs_ayant_joue.get(j.pseudo, False) for j in actifs)

        return mises_equivalentes and tous_ont_joue

    def annoncer_resultats(self) -> EtatPartie:
        joueurs_en_jeu = [j for j in self.table.joueurs if j.actif or j.mise > 0]
        
        if len(joueurs_en_jeu) <= 1:
            if joueurs_en_jeu:
                gagnant = joueurs_en_jeu[0]
                gagnant.solde += self.comptage.pot
                self.etat.resultats = [{
                    "pseudo": gagnant.pseudo,
                    "main": [str(c) for c in gagnant.main],
                    "description": "Gagne car les autres se sont couchés"
                }]
            self.comptage.pot = 0
            self.etat.finie = True
            self._mettre_a_jour_etat()
            self.etat.rejouer = {j.pseudo: None for j in self.table.joueurs}
            return self.etat

        scores = {}
        for j in joueurs_en_jeu:
            cartes_totales = j.main + self.table.board
            evaluateur = EvaluateurMain(cartes_totales)
            resultat = evaluateur.evalue_main()
            scores[j] = resultat

        gagnants = [joueurs_en_jeu[0]]
        for j in joueurs_en_jeu[1:]:
            cmp = EvaluateurMain.comparer_mains(scores[j], scores[gagnants[0]])
            if cmp == 1:
                gagnants = [j]
            elif cmp == 0:
                gagnants.append(j)

        self.etat.resultats = []
        if self.comptage.pot > 0:
            part = self.comptage.pot // len(gagnants)
            for j in gagnants:
                j.solde += part
                self.etat.resultats.append({
                    "pseudo": j.pseudo,
                    "main": [str(c) for c in j.main],
                    "description": f"Gagne {part} jetons avec {scores[j].combinaison} et kickers {scores[j].tiebreaker_cards}"
                })
            self.comptage.pot = 0

        self.etat.finie = True
        self.etat.rejouer = {j.pseudo: None for j in self.table.joueurs}
        self._mettre_a_jour_etat()
        return self.etat

    def gestion_rejouer(self) -> bool:
        """
        Prépare la partie pour une nouvelle main, réinitialise tout l'état.
        Intègre automatiquement les joueurs de la liste d'attente.
        Retourne True si la partie pourrait être relancée (>=2 joueurs), sinon False.
        """
        # Supprimer les joueurs hors-solde
        self.table.joueurs = [j for j in self.table.joueurs if j.solde >= Partie.GROSSE_BLIND]

        # Réinitialiser tous les joueurs restants
        for j in self.table.joueurs:
            j.mise = 0
            j.actif = True
            j.main = []

        # Intégrer les joueurs de la liste d'attente
        for j in self.etat.liste_attente:
            joueur = Joueur(pseudo=j['pseudo'], solde=j['solde'])
            self.table.ajouter_joueur(joueur)
            joueur.actif = True
        # Vider la liste d'attente
        self.etat.liste_attente.clear()

        # Réinitialiser pot, board et comptage
        self.table.board = []
        self.comptage = Comptage()
        self.distrib = Distrib(self.table.joueurs)
        self.tour_actuel = "preflop"
        self.mise_max = 0
        self.indice_joueur_courant = 0
        self.etat.finie = True
        self._mettre_a_jour_etat()

        for pseudo in self.etat.rejouer:
            self.etat.rejouer[pseudo] = None
        self.etat.finie = True  # avant la relance
        self._mettre_a_jour_etat()


        if len(self.table.joueurs) >= 2:

            self.initialiser_blinds()
            self.etat.finie = False  # La partie repart
            self._mettre_a_jour_etat()
            return True  # Partie relancée

        return False  # Pas assez de joueurs, partie reste en pause


    def integrer_attente(self):
        """
        Intègre automatiquement tous les joueurs en liste d'attente.
        """
        for j in self.partie.etat.liste_attente:
            joueur = Joueur(pseudo=j['pseudo'], solde=j['solde'])
            self.partie.table.ajouter_joueur(joueur)
            joueur.actif = True
        self.partie.etat.liste_attente.clear()

    def ajouter_a_liste_attente(self, joueur: Joueur):
        self.etat.liste_attente.append({
            "pseudo": joueur.pseudo,
            "solde": joueur.solde,
            "jeton": joueur.jeton if hasattr(joueur, "jeton") else None
        })

    def reponse_rejouer(self, pseudo: str, veut_rejouer: bool) -> EtatPartie:
        """Un joueur répond s’il veut rejouer ou non."""
        self.etat.rejouer[pseudo] = veut_rejouer

        # Si tous les joueurs ont répondu, on tente de relancer

        if all(v is not None for v in self.etat.rejouer.values()):

            self._relancer_si_possible()

        self._mettre_a_jour_etat()
        return self.etat

    def _relancer_si_possible(self):
        """Vérifie qui veut rejouer et relance une nouvelle main si possible."""
        # Retirer les joueurs qui ne veulent pas rejouer
        self.table.joueurs = [j for j in self.table.joueurs if self.etat.rejouer.get(j.pseudo)]

        # Intégrer les nouveaux joueurs en attente
        for j in self.etat.liste_attente:
            joueur = Joueur(pseudo=j["pseudo"], solde=j["solde"])
            self.table.ajouter_joueur(joueur)
        self.etat.liste_attente.clear()


        # Si au moins 2 joueurs, on relance la partie
        if len(self.table.joueurs) >= 2:

            self.gestion_rejouer()