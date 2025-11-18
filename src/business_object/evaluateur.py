from src.business_object.cartes import Carte, combinaisons, valeurs
from collections import Counter
from typing import List, Optional, Dict, Tuple


class ResultatMain:
    def __init__(self, combinaison, tiebreaker_cards)->None:
        self.combinaison = combinaison
        # tiebreaker_cards contient désormais des enums valeurs.* directement
        self.tiebreaker_cards = tiebreaker_cards

    @property
    def value(self)->int:
        return self.combinaison.value


class EvaluateurMain:
    valeur_order = {
        valeurs.DEUX: 2, valeurs.TROIS: 3, valeurs.QUATRE: 4,
        valeurs.CINQ: 5, valeurs.SIX: 6, valeurs.SEPT: 7,
        valeurs.HUIT: 8, valeurs.NEUF: 9, valeurs.DIX: 10,
        valeurs.VALET: 11, valeurs.DAME: 12, valeurs.ROI: 13,
        valeurs.AS: 14
    }

    def __init__(self, cartes: list[Carte])->None:
        if len(cartes) < 5 or len(cartes) > 7:
            raise ValueError("Il faut entre 5 et 7 cartes pour évaluer une main.")
        self.cartes = cartes

    def _valeurs_numeriques(self)->List[int]:
        return sorted([self.valeur_order[c.valeur] for c in self.cartes], reverse=True)

    def _compter_occurrences(self)->Counter[int]:
        counts = Counter(self._valeurs_numeriques())
        return counts

    def _is_flush(self)->Tuple[bool, List[valeurs]]:
        couleurs_count = Counter(c.couleur for c in self.cartes)
        for couleur, count in couleurs_count.items():
            if count >= 5:
                flush_vals = [c.valeur for c in self.cartes if c.couleur == couleur]
                return True, flush_vals
        return False, []

    def _is_straight(self, valeurs)->Tuple[bool, List[int]]:
        vals = sorted(set(valeurs))
        for i in range(len(vals) - 4):
            if vals[i + 4] - vals[i] == 4:
                return True, vals[i:i + 5]
        # quinte basse A-2-3-4-5
        if 14 in vals:
            low_vals = [1 if v == 14 else v for v in vals]
            low_vals = sorted(set(low_vals))
            for i in range(len(low_vals) - 4):
                if low_vals[i + 4] - low_vals[i] == 4:
                    return True, [v if v != 1 else 14 for v in low_vals[i:i + 5]]
        return False, []

    def _numerique_to_enum(self, valeur_num)-> Optional[valeurs]:
        """Convertit une valeur numérique en enum valeurs."""
        for enum_val, num in self.valeur_order.items():
            if num == valeur_num:
                return enum_val
        return None 

    def evalue_main(self)->ResultatMain:
        counts = self._compter_occurrences()
        valeurs_list = self._valeurs_numeriques()
        is_flush, flush_vals = self._is_flush()
        is_straight, straight_vals = self._is_straight(valeurs_list)

        # Quinte flush royale / Quinte flush
        if is_flush and is_straight:
            flush_straight = [self.valeur_order[v] for v in flush_vals if self.valeur_order[v] in straight_vals]
            if set([10, 11, 12, 13, 14]).issubset(flush_straight):
                return ResultatMain(combinaisons.QUINTE_FLUSH_ROYALE, [valeurs.AS])
            top_flush_straight = sorted(flush_straight, reverse=True)
            return ResultatMain(
                combinaisons.QUINTE_FLUSH,
                [self._numerique_to_enum(v) for v in top_flush_straight]
            )

        # Carré
        if 4 in counts.values():
            carre = [val for val, cnt in counts.items() if cnt == 4][0]
            kicker = max([v for v in valeurs_list if v != carre])
            return ResultatMain(
                combinaisons.CARRE,
                [self._numerique_to_enum(carre), self._numerique_to_enum(kicker)]
            )

        # Full
        if 3 in counts.values() and 2 in counts.values():
            brelan = max([val for val, cnt in counts.items() if cnt == 3])
            paire = max([val for val, cnt in counts.items() if cnt == 2])
            return ResultatMain(
                combinaisons.FULL,
                [self._numerique_to_enum(brelan), self._numerique_to_enum(paire)]
            )

        # Flush
        if is_flush:
            top5 = sorted([self.valeur_order[v] for v in flush_vals], reverse=True)[:5]
            return ResultatMain(
                combinaisons.COULEUR,
                [self._numerique_to_enum(v) for v in top5]
            )

        # Straight
        if is_straight:
            return ResultatMain(
                combinaisons.QUINTE,
                [self._numerique_to_enum(v) for v in sorted(straight_vals, reverse=True)]
            )

        # Brelan
        if 3 in counts.values():
            brelan = max([val for val, cnt in counts.items() if cnt == 3])
            kickers = sorted([v for v in valeurs_list if v != brelan], reverse=True)[:2]
            return ResultatMain(
                combinaisons.BRELAN,
                [self._numerique_to_enum(brelan)] + [self._numerique_to_enum(k) for k in kickers]
            )

        # Double paire
        if list(counts.values()).count(2) >= 2:
            paires = sorted([val for val, cnt in counts.items() if cnt == 2], reverse=True)[:2]
            kicker = max([v for v in valeurs_list if v not in paires])
            return ResultatMain(
                combinaisons.DOUBLE_PAIRE,
                [self._numerique_to_enum(v) for v in paires + [kicker]]
            )

        # Paire
        if 2 in counts.values():
            paire = max([val for val, cnt in counts.items() if cnt == 2])
            kickers = sorted([v for v in valeurs_list if v != paire], reverse=True)[:3]
            return ResultatMain(
                combinaisons.PAIRE,
                [self._numerique_to_enum(paire)] + [self._numerique_to_enum(k) for k in kickers]
            )

        # Hauteur
        top5 = valeurs_list[:5]
        return ResultatMain(
            combinaisons.HAUTEUR,
            [self._numerique_to_enum(v) for v in top5]
        )

    @staticmethod
    def comparer_mains(main1, main2)->int:
        if main1.value > main2.value:
            return 1
        elif main1.value < main2.value:
            return -1
        else:
            # comparer les tiebreaker_cards
            for c1, c2 in zip(main1.tiebreaker_cards, main2.tiebreaker_cards):
                if EvaluateurMain.valeur_order[c1] > EvaluateurMain.valeur_order[c2]:
                    return 1
                elif EvaluateurMain.valeur_order[c1] < EvaluateurMain.valeur_order[c2]:
                    return -1
            return 0

"""
class ComparaisonMain(enum):
    PlusForte,
    Moins,
    Egale
"""