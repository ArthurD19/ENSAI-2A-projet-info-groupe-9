from src.business_object.joueurs import Joueur
from src.business_object.distrib import Distrib
from src.business_object.comptage import Comptage
from src.business_object.evaluateur import EvaluateurMain

from src.dao.statistique_dao import StatistiqueDao
from src.dao.joueur_dao import JoueurDao


class EtatPartie:
    def __init__(self):
        self.id_partie: int = -1
        self.tour_actuel: str = "preflop"
        self.joueurs: list[dict] = []  # contient : pseudo, solde, mise, actif
        self.board: list[str] = []
        self.pot: int = 0
        self.pots_secondaires: dict = {}
        self.mise_max: int = 0
        self.joueur_courant: str | None = None
        self.finie: bool = True   # True si la partie est terminée
        self.resultats: list[dict] = []  # liste des gagnants avec info sur leur main et kickers
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
        # suppression du champ redondant index_joueur_courant

    # ---------------------------
    # Synchronisation état -> vue
    # ---------------------------
    def _mettre_a_jour_etat(self):
        # synchronise l'objet métier vers l'objet d'état exposé
        self.etat.id_partie = getattr(self, "id", None)
        self.etat.tour_actuel = self.tour_actuel
        self.etat.joueurs = [
            {"pseudo": j.pseudo, "solde": j.solde, "mise": j.mise, "actif": j.actif}
            for j in self.table.joueurs
        ]
        self.etat.board = [str(c) for c in self.table.board]
        self.etat.pot = self.comptage.pot
        # pots secondaires (clé pseudo -> montant)
        try:
            # comptage.pots_perso est un dict mapping joueur->montant
            self.etat.pots_secondaires = {
                j.pseudo: montant for j, montant in self.comptage.pots_perso.items()}
        except Exception:
            # fallback si structure différente
            self.etat.pots_secondaires = getattr(self.comptage, "pots_secondaires", {})

        self.etat.mise_max = self.mise_max

        # Propager resultats/rejouer/liste_attente s'ils existent
        self.etat.resultats = getattr(self.etat, "resultats", [])
        self.etat.rejouer = getattr(self.etat, "rejouer", {})
        self.etat.liste_attente = getattr(self.etat, "liste_attente", [])

        # Si la partie est finie, il ne doit pas y avoir de joueur courant
        if getattr(self.etat, "finie", False):
            self.etat.joueur_courant = None
        else:
            if self.table.joueurs and 0 <= self.indice_joueur_courant < len(self.table.joueurs):
                self.etat.joueur_courant = self.table.joueurs[self.indice_joueur_courant].pseudo
            else:
                self.etat.joueur_courant = None

    # ---------------------------
    # Initialisation des blinds
    # ---------------------------
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
        # Avancer le dealer pour la main suivante (comportement conservé)
        self.table.indice_dealer = (self.table.indice_dealer + 1) % nb_joueurs

        # Initialiser le tracking des joueurs ayant joué (actifs non all-in)
        self.joueurs_ayant_joue = {
            j.pseudo: False for j in self.table.joueurs if j.actif and j.solde > 0}

        self.etat.finie = False
        self._mettre_a_jour_etat()

    # ---------------------------
    # Passer au tour suivant
    # ---------------------------
    def passer_tour(self):
        # Consolider mises personnelles dans le comptage
        for j in self.table.joueurs:
            if j.mise > 0:
                self.comptage.ajouter_pot_perso(j, j.mise)
                j.mise = 0
        self.comptage.ajouter_pot()
        self.mise_max = 0

        # Avancer d'un tour
        if self.tour_actuel == "preflop":
            self.distrib.distribuer_flop()
            # copier la liste pour ne pas partager la référence interne
            self.table.board = list(self.distrib.flop)
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
            # annoncer_resultats appellera _mettre_a_jour_etat
            self.annoncer_resultats()
            return  # annoncer_resultats mettra l'état à jour

        # Réinitialiser les flags de qui a joué : seuls les joueurs actifs non all-in devront jouer
        self.joueurs_ayant_joue = {
            j.pseudo: False for j in self.table.joueurs if j.actif and j.solde > 0}

        # Considérer que les joueurs all-in ont déjà "joué"
        for j in self.table.joueurs:
            if j.actif and j.solde == 0:
                self.joueurs_ayant_joue[j.pseudo] = True

        # Si après avoir avancé, tous les joueurs actifs sont all-in, avancer automatiquement
        # jusqu'à showdown (flop->turn->river->showdown)
        while self.tour_actuel != "fin":
            actifs = [j for j in self.table.joueurs if j.actif]
            if not actifs:
                break

            if all(j.solde == 0 for j in actifs):
                # consolider encore avant d'avancer (sécurité)
                for j in self.table.joueurs:
                    if j.mise > 0:
                        self.comptage.ajouter_pot_perso(j, j.mise)
                        j.mise = 0
                self.comptage.ajouter_pot()

                if self.tour_actuel == "flop":
                    self.distrib.distribuer_turn()
                    self.table.board.append(self.distrib.turn)
                    self.tour_actuel = "turn"
                    # reset flags (toujours all-in => pas besoin)
                    continue
                elif self.tour_actuel == "turn":
                    self.distrib.distribuer_river()
                    self.table.board.append(self.distrib.river)
                    self.tour_actuel = "river"
                    continue
                elif self.tour_actuel == "river":
                    self.tour_actuel = "fin"
                    self.annoncer_resultats()
                    return
                else:
                    # si preflop, on a déjà transformé en flop en haut de boucle
                    pass
            else:
                # au moins un joueur peut encore agir → on s'arrête ici
                break

        # Mettre à jour l'état pour que l'API/UI voie la nouvelle situation (tour, board, etc.)
        self._mettre_a_jour_etat()

    # ---------------------------
    # Actions d'un joueur (miser / suivre / all-in / se coucher)
    # ---------------------------
    def actions_joueur(self, pseudo: str, action: str, montant: int | None = None):
        # PROTECTION : ne rien faire si la main est terminée
        if getattr(self.etat, "finie", False):
            return self.etat

        joueur = next((j for j in self.table.joueurs if j.pseudo == pseudo), None)
        if not joueur or not joueur.actif:
            return self.etat

        # Marquer que le joueur a joué ce tour (sera ajusté si raise)
        self.joueurs_ayant_joue[joueur.pseudo] = True

        mise_max_avant = self.mise_max

        # Effectuer l'action demandée
        if action == "miser" and montant is not None:
            joueur.miser(montant)
            self.mise_max = joueur.mise
            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_mises")

        elif action == "suivre":
            joueur.suivre(self.mise_max)
            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_suivis")

        elif action == "all-in":
            # mise le reste du solde
            joueur.miser(joueur.solde)
            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_all_in")
            # mise_max doit devenir le max entre l'ancienne et la mise du joueur
            self.mise_max = max(self.mise_max, joueur.mise)

        elif action == "se_coucher":
            # conserver la mise actuelle dans le pot (consolidation)
            self.comptage.pot += joueur.mise
            joueur.se_coucher()
            joueur.mise = 0
            self.stats_dao.incrementer_statistique(joueur.pseudo, "nombre_folds")

            # Si un seul joueur reste actif, on annonce le résultat directement
            actifs = [j for j in self.table.joueurs if j.actif]
            if len(actifs) == 1:
                self.indice_joueur_courant = self.table.joueurs.index(actifs[0])
                gagnant = actifs[0]

                if gagnant.mise > 0:
                    self.comptage.pot += gagnant.mise
                    gagnant.mise = 0

                # S'assurer que l'état final est propre : marquer fin, invalider joueur courant
                self.etat.finie = True
                self.indice_joueur_courant = -1
                self.annoncer_resultats()
                # annoncer_resultats appelle _mettre_a_jour_etat et retourne
                return self.etat

        # Si la mise_max a augmenté (raise / all-in qui augmente),
        # alors tous les joueurs actifs non all-in doivent rejouer.
        if self.mise_max > mise_max_avant:
            self.joueurs_ayant_joue = {
                j.pseudo: False
                for j in self.table.joueurs
                if j.actif and j.solde > 0
            }
            # Marquer le raiseur (ou all-in) comme ayant déjà joué
            self.joueurs_ayant_joue[joueur.pseudo] = True

        # Considérer qu'un joueur qui est all-in a "joué"
        for j in self.table.joueurs:
            if j.solde == 0 and j.actif:
                self.joueurs_ayant_joue[j.pseudo] = True

        # Vérifier si le tour est terminé (all-in ou tous ont joué)
        if self._tour_termine():
            self.passer_tour()
            return self.etat

        # Déterminer le prochain joueur actif (skip: non-actif, all-in, ou qui a déjà joué)
        self._joueur_suivant()

        self._mettre_a_jour_etat()
        return self.etat

    # ---------------------------
    # Vérifier fin du tour
    # ---------------------------
    def _tour_termine(self) -> bool:
        actifs = [j for j in self.table.joueurs if j.actif]
        if len(actifs) <= 1:
            return True

        limite_max = self.mise_max_autorisee()
        # Si tous les joueurs actifs sont all-in, le tour est terminé
        if all(j.solde == 0 or j.mise == limite_max for j in actifs):
            return True

        mises_actifs = [j.mise for j in actifs]
        mises_equivalentes = len(set(mises_actifs)) == 1

        # Considérer qu'un joueur qui est all-in a "joué"
        tous_ont_joue = all(
            self.joueurs_ayant_joue.get(j.pseudo, False) or j.solde == 0
            for j in actifs
        )

        return mises_equivalentes and tous_ont_joue

    # ---------------------------
    # Trouver le prochain joueur qui doit agir
    # ---------------------------
    def _joueur_suivant(self):
        """
        Met à jour self.indice_joueur_courant pour pointer sur le prochain joueur actif
        qui doit encore jouer (skip all-in, skip folds).
        Si la main est finie, met joueur_courant = None.
        """
        if getattr(self.etat, "finie", False):
            self.indice_joueur_courant = -1
            self.etat.joueur_courant = None
            return

        nb_joueurs = len(self.table.joueurs)
        if nb_joueurs == 0:
            self.indice_joueur_courant = -1
            self.etat.joueur_courant = None
            return

        start = self.indice_joueur_courant if self.indice_joueur_courant >= 0 else 0
        next_idx = (start + 1) % nb_joueurs
        boucle = 0
        while boucle < nb_joueurs:
            cand = self.table.joueurs[next_idx]
            a_deja_joue = self.joueurs_ayant_joue.get(cand.pseudo, False)
            # Conditions pour s'arrêter sur ce joueur :
            # - il est actif
            # - il n'est pas all-in (solde > 0)
            # - il n'a pas encore joué ce tour
            if cand.actif and cand.solde > 0 and not a_deja_joue:
                self.indice_joueur_courant = next_idx
                self.etat.joueur_courant = cand.pseudo
                return
            next_idx = (next_idx + 1) % nb_joueurs
            boucle += 1

        # Aucun joueur trouvé : soit tous ont joué, soit tous sont all-in, soit pas d'actifs.
        # Si le tour est terminé, on le fait avancer automatiquement.
        if self._tour_termine():
            # appeler passer_tour pour faire avancer le jeu (flop/turn/river/fin)
            self.passer_tour()
            return

        # Si on arrive ici : pas de joueur disponible mais l    e tour n'est pas marqué terminé
        # (ex: cas improbable de désynchronisation). On établit joueur_courant à None.
        self.indice_joueur_courant = -1
        self.etat.joueur_courant = None

    # ---------------------------
    # Annoncer résultats / showdown
    # ---------------------------
    def annoncer_resultats(self) -> EtatPartie:
        self.etat.resultats = []

        for j in self.table.joueurs:
            self.stats_dao.incrementer_statistique(j.pseudo, "nombre_total_mains_jouees")
            self.stats_dao.incrementer_statistique(j.pseudo, "nombre_mains_jouees_session")

        joueurs_en_jeu = [j for j in self.table.joueurs if j.actif or j.mise > 0]

        # Mettre à jour le portefeuille de TOUS les joueurs en base
        for j in joueurs_en_jeu:
            JoueurDao().mettre_a_jour_solde(j.pseudo, j.solde)

        # Cas : un seul joueur en jeu => gagne immédiatement
        if len(joueurs_en_jeu) <= 1:
            if joueurs_en_jeu:
                gagnant = joueurs_en_jeu[0]
                gagnant.solde += self.comptage.pot

                # Incrémenter stats de victoire pour ce joueur
                self.stats_dao.incrementer_statistique(gagnant.pseudo, "nombre_victoire_abattage")

                self.etat.resultats = [{
                    "pseudo": gagnant.pseudo,
                    "main": [str(c) for c in gagnant.main],
                    "description": "Gagne car les autres se sont couchés."
                }]

            self.comptage.pot = 0
            self.etat.finie = True
            self.indice_joueur_courant = -1
            self._mettre_a_jour_etat()
            self.etat.rejouer = {j.pseudo: None for j in self.table.joueurs}
            for j in self.table.joueurs:
                JoueurDao().mettre_a_jour_solde(j.pseudo, j.solde)
            return self.etat

        # Cas normal : showdown
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

        if self.comptage.pot > 0:
            part = self.comptage.pot // len(gagnants)
            for j in gagnants:
                j.solde += part

                # Incrémenter stats de victoire pour le gagnant
                self.stats_dao.incrementer_statistique(j.pseudo, "nombre_victoire_abattage")

                self.etat.resultats.append({
                    "pseudo": j.pseudo,
                    "main": [str(c) for c in j.main],
                    "description": "Gagne parce qu'il avait une meilleure combinaison"
                })
            self.comptage.pot = 0

        # Marquer fin et préparer rejouer
        self.etat.finie = True
        self.indice_joueur_courant = -1
        self.etat.rejouer = {j.pseudo: None for j in self.table.joueurs}
        self._mettre_a_jour_etat()
        for j in self.table.joueurs:
            JoueurDao().mettre_a_jour_solde(j.pseudo, j.solde)
        return self.etat

    # ---------------------------
    # Gestion du relancement / nouvelle main
    # ---------------------------
    def gestion_rejouer(self) -> bool:
        """Prépare la partie pour une nouvelle main, réinitialise tout l'état."""
        # Filtrer les joueurs sans solde suffisant
        joueurs_valides = [j for j in self.table.joueurs if j.solde >= Partie.GROSSE_BLIND]

        # Intégrer les joueurs en attente (sans doublon et avec solde suffisant)
        pseudos_deja_presents = {j.pseudo for j in joueurs_valides}
        for j in list(self.etat.liste_attente):
            if j['solde'] >= Partie.GROSSE_BLIND and j['pseudo'] not in pseudos_deja_presents:
                joueur = Joueur(pseudo=j['pseudo'], solde=j['solde'])
                joueurs_valides.append(joueur)
                pseudos_deja_presents.add(j['pseudo'])

        self.etat.liste_attente.clear()
        self.table.joueurs = joueurs_valides

        # Si pas assez de joueurs, marquer comme finie
        if len(self.table.joueurs) < 2:
            self.etat.finie = True
            self._mettre_a_jour_etat()
            return False

        # Réinitialiser les joueurs restants
        for j in self.table.joueurs:
            j.mise = 0
            j.actif = True
            j.main = []

        # Réinitialiser pot, board et comptage
        self.table.board = []
        self.comptage = Comptage()
        self.distrib = Distrib(self.table.joueurs)
        self.tour_actuel = "preflop"
        self.mise_max = 0
        self.indice_joueur_courant = 0

        # Relancer la partie
        self.initialiser_blinds()
        return True

    # ---------------------------
    # Liste d'attente / intégration
    # ---------------------------
    def integrer_attente(self):
        """
        Intègre automatiquement tous les joueurs en liste d'attente.
        """
        for j in list(self.etat.liste_attente):
            joueur = Joueur(pseudo=j['pseudo'], solde=j['solde'])
            self.table.ajouter_joueur(joueur)
            joueur.actif = True
        self.etat.liste_attente.clear()

    def ajouter_a_liste_attente(self, joueur: Joueur):
        self.etat.liste_attente.append({
            "pseudo": joueur.pseudo,
            "solde": joueur.solde,
            "jeton": joueur.jeton if hasattr(joueur, "jeton") else None
        })

    # ---------------------------
    # Reponse après la main : rejouer or not
    # ---------------------------
    def reponse_rejouer(self, pseudo: str, veut_rejouer: bool) -> EtatPartie:
        """Un joueur répond s’il veut rejouer ou non."""
        joueur = next((j for j in self.table.joueurs if j.pseudo == pseudo), None)
        if not joueur:
            return self.etat

        # Si le joueur n'a pas assez de jetons, forcer "Non"
        if joueur.solde < Partie.GROSSE_BLIND:
            veut_rejouer = False

        self.etat.rejouer[pseudo] = veut_rejouer

        # Si tous les joueurs ont répondu, on tente de relancer
        if all(v is not None for v in self.etat.rejouer.values()):
            self._relancer_si_possible()
        self._mettre_a_jour_etat()
        return self.etat

    def _relancer_si_possible(self):
        """Vérifie qui veut rejouer et relance une nouvelle main si possible."""
        # Vérifier que tous les joueurs ont répondu
        if not all(v is not None for v in self.etat.rejouer.values()):
            return

        # Filtrer les joueurs sans solde suffisant
        joueurs_valides = [j for j in self.table.joueurs if j.solde >= Partie.GROSSE_BLIND]

        # Ajouter les joueurs en liste d'attente avec solde suffisant
        pseudos_en_attente = {
            j['pseudo'] for j in self.etat.liste_attente if j['solde'] >= Partie.GROSSE_BLIND}
        pseudos_rejouent = {pseudo for pseudo, rejoue in self.etat.rejouer.items() if rejoue}

        # Si moins de 2 joueurs combinés veulent rejouer / sont en attente, on ne relance pas
        if len(pseudos_rejouent | pseudos_en_attente) < 2:
            self.etat.finie = True
            self._mettre_a_jour_etat()
            return

        # Sinon, construire la nouvelle table avec ceux qui veulent rejouer
        pseudos_deja_presents = set()
        joueurs_rejouent = []
        for j in joueurs_valides:
            if self.etat.rejouer.get(j.pseudo, False) and j.pseudo not in pseudos_deja_presents:
                joueurs_rejouent.append(j)
                pseudos_deja_presents.add(j.pseudo)

        # Intégrer les joueurs en attente
        for j in list(self.etat.liste_attente):
            if j["solde"] >= Partie.GROSSE_BLIND and j["pseudo"] not in pseudos_deja_presents:
                joueur = Joueur(pseudo=j["pseudo"], solde=j["solde"])
                joueurs_rejouent.append(joueur)
                pseudos_deja_presents.add(j["pseudo"])

        self.etat.liste_attente.clear()
        self.table.joueurs = joueurs_rejouent
        self.etat.rejouer = {}

        # Relancer la partie si encore au moins 2 joueurs
        if len(self.table.joueurs) >= 2:
            self.gestion_rejouer()
        else:
            self.etat.finie = True
            self._mettre_a_jour_etat()

    # ---------------------------
    # our ne pas gerer les pots secondaire
    # ---------------------------
    def mise_max_autorisee(self) -> int:
        return min(
            j.solde + j.mise
            for j in self.table.joueurs
            if j.actif
        )
