from business_object.cartes import Carte, combinaisons, valeurs

class EvaluateurMain:
    """
    Évalue une main de poker Texas Hold'em (7 cartes max).
    Prend en entrée 5 à 7 cartes (2 privées + 5 communes).
    Retourne la meilleure combinaison.
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
        """Retourne les valeurs numériques triées du plus grand au plus petit."""
        return sorted([self.valeur_order[c.valeur] for c in self.cartes], reverse=True)

    def _compter_occurrences(self):
        """Compte combien de fois chaque valeur apparaît dans la main."""
        counts = {}
        for c in self.cartes:
            v = self.valeur_order[c.valeur]
            counts[v] = counts.get(v, 0) + 1
        return counts

    def _is_flush(self):
        """Vérifie si la main contient au moins 5 cartes de la même couleur."""
        couleurs_count = {}
        for c in self.cartes:
            couleurs_count[c.couleur] = couleurs_count.get(c.couleur, 0) + 1
        return max(couleurs_count.values()) >= 5

    def _is_straight(self, valeurs):
        """Vérifie si la main contient une suite de 5 cartes consécutives."""
        valeurs = sorted(set(valeurs))
        for i in range(len(valeurs) - 4):
            if valeurs[i + 4] - valeurs[i] == 4:
                return True
        # Quinte basse A-2-3-4-5
        if 14 in valeurs:
            quinte_basse = [1 if v == 14 else v for v in valeurs]
            quinte_basse = sorted(set(quinte_basse))
            for i in range(len(quinte_basse) - 4):
                if quinte_basse[i + 4] - quinte_basse[i] == 4:
                    return True
        return False

    def evalue_main(self):
        """
        Détermine la meilleure combinaison de la main.
        Retourne une valeur de 'combinaisons'.
        """
        counts = self._compter_occurrences()
        valeurs_counts = sorted(counts.values(), reverse=True)
        valeurs_list = self._valeurs_numeriques()
        is_flush = self._is_flush()
        is_straight = self._is_straight(valeurs_list)

        if is_flush and set([10, 11, 12, 13, 14]).issubset(valeurs_list):
            return combinaisons.QUINTE_FLUSH_ROYALE
        elif is_flush and is_straight:
            return combinaisons.QUINTE_FLUSH
        elif 4 in valeurs_counts:
            return combinaisons.CARRE
        elif 3 in valeurs_counts and 2 in valeurs_counts:
            return combinaisons.FULL
        elif is_flush:
            return combinaisons.COULEUR
        elif is_straight:
            return combinaisons.QUINTE
        elif 3 in valeurs_counts:
            return combinaisons.BRELAN
        elif valeurs_counts.count(2) == 2:
            return combinaisons.DOUBLE_PAIRE
        elif 2 in valeurs_counts:
            return combinaisons.PAIRE
        else:
            return combinaisons.HAUTEUR

    @staticmethod
    def comparer_mains(main1, main2):
        """
        Compare deux combinaisons de mains :
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
