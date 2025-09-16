from cartes import Carte, valeurs, combinaisons


class EvaluateurMain:
    """
    Évalue une main de poker Texas Hold'em.
    Prend en entrée 5 à 7 cartes (2 privées + 5 communes).
    Retourne le rang de la meilleure combinaison trouvée.
    """

    valeur_order = {
        valeurs.DEUX: 2, valeurs.TROIS: 3, valeurs.QUATRE: 4,
        valeurs.CINQ: 5, valeurs.SIX: 6, valeurs.SEPT: 7,
        valeurs.HUIT: 8, valeurs.NEUF: 9, valeurs.DIX: 10,
        valeurs.VALET: 11, valeurs.DAME: 12, valeurs.ROI: 13,
        valeurs.AS: 14
    }

    def __init__(self, cartes: list[Carte]):
        if len(cartes) < 5 or len(cartes) > 7:
            raise ValueError("Il faut entre 5 et 7 cartes pour évaluer une main.")
        self.cartes = cartes

    def _valeurs_numeriques(self):
        """Retourne les valeurs des cartes en nombres triés (du plus grand au plus petit)."""
        return sorted([self.valeur_order[c.valeur] for c in self.cartes], reverse=True)

    def _compter_occurrences(self):
        """Compte combien de fois chaque valeur apparaît."""
        counts = {}
        for c in self.cartes:
            v = self.valeur_order[c.valeur]
            counts[v] = counts.get(v, 0) + 1
        return counts

    def _is_flush(self):
        """Vérifie si toutes les cartes ont la même couleur (au moins 5 cartes)."""
        couleurs = {}
        for c in self.cartes:
            couleurs[c.couleur] = couleurs.get(c.couleur, 0) + 1
        return max(couleurs.values()) >= 5

    def _is_straight(self, valeurs_list):
        """Vérifie si les cartes forment une suite (quinte)."""
        valeurs_uniques = sorted(set(valeurs_list))
        # Cas particulier : A peut compter comme 1 dans une quinte A-2-3-4-5
        if 14 in valeurs_uniques:
            valeurs_uniques.append(1)

        for i in range(len(valeurs_uniques) - 4):
            if valeurs_uniques[i+4] - valeurs_uniques[i] == 4:
                return True
        return False

    def evalue_main(self):
        """
        Détermine la meilleure combinaison de la main.
        """
        counts = self._compter_occurrences()
        valeurs_counts = sorted(counts.values(), reverse=True)
        valeurs_list = self._valeurs_numeriques()

        is_flush = self._is_flush()
        is_straight = self._is_straight(valeurs_list)

        # Quinte Flush Royale
        if is_flush and set([10, 11, 12, 13, 14]).issubset(valeurs_list):
            return combinaisons.QUINTE_FLUSH_ROYALE
        # Quinte Flush
        if is_flush and is_straight:
            return combinaisons.QUINTE_FLUSH
        # Carré
        if 4 in valeurs_counts:
            return combinaisons.CARRE
        # Full (3 + 2)
        if 3 in valeurs_counts and 2 in valeurs_counts:
            return combinaisons.FULL
        # Couleur
        if is_flush:
            return combinaisons.COULEUR
        # Suite
        if is_straight:
            return combinaisons.QUINTE
        # Brelan
        if 3 in valeurs_counts:
            return combinaisons.BRELAN
        # Double paire
        if valeurs_counts.count(2) == 2:
            return combinaisons.DOUBLE_PAIRE
        # Paire
        if 2 in valeurs_counts:
            return combinaisons.PAIRE

        # Sinon hauteur
        return combinaisons.HAUTEUR

    @staticmethod
    def comparer_mains(main1, main2):
        """
        Compare deux mains :
        - retourne 1 si main1 gagne
        - retourne -1 si main2 gagne
        - retourne 0 si égalité
        """
        if main1.value > main2.value:
            return 1
        elif main1.value < main2.value:
            return -1
        else:
            return 0
