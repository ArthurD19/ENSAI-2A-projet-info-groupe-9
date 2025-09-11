
# Diagramme de classes des objets métiers

Ce diagramme est codé avec [mermaid](https://mermaid.js.org/syntax/classDiagram.html) :

* avantage : facile à coder
* inconvénient : on ne maîtrise pas bien l'affichage

Pour afficher ce diagramme dans VScode :

* à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
* rechercher `mermaid`
  * installer l'extension **Markdown Preview Mermaid Support**
* revenir sur ce fichier
  * faire **CTRL + K**, puis **V**

```mermaid
classDiagram
    class Couleur {
        PIQUE
        TREFLE
        CARREAU
        COEUR
    }

    class Valeur {
        DEUX
        TROIS
        QUATRE
        CINQ
        SIX
        SEPT
        HUIT
        NEUF
        DIX
        VALET
        DAME
        ROI
        AS
    }

    class RangMain {
        HAUTE_CARTE
        PAIRE
        DEUX_PAIRES
        BRELANT
        SUITE
        COULEUR
        FULL
        CARRE
        SUITE_COULEUR
        QUINTE_ROYALE
    }

    class Carte {
        +valeur : Valeur
        +couleur : Couleur
        +__repr__() : str
        +__lt__(autre : Carte) : bool
        +__eq__(autre : Carte) : bool
    }

    class Paquet {
        -cartes : List<Carte>
        +remettre_a_zero() : None
        +melanger() : None
        +tirer() : Carte
        +taille() : int
    }

    class Joueur {
        +pseudo : str
        +solde : Decimal
        +cartes_privees : List<Carte>
        +en_partie : bool
        +mise_courante : Decimal
        +recevoir_carte(carte : Carte) : None
        +se_coucher() : None
        +check(mise_maximale : Decimal) : None
        +suivre(mise_maximale : Decimal) : None
        +miser(montant : Decimal) : None
        +reset_pour_nouvelle_main() : None
    }

    class Table {
        +nom : str
        +joueurs : List<Joueur>
        +petite_mise : Decimal
        +grosse_mise : Decimal
        +asseoir(joueur : Joueur) : None
        +quitter(joueur : Joueur) : None
        +nombre_joueurs() : int
    }

    class Partie {
        +table : Table
        +paquet : Paquet
        +cartes_communes : List<Carte>
        +pot : Decimal
        +index_dealer : int
        +position_actuelle : int
        +phase_index : int
        +demarrer() : None
        +passer_phase() : None
        +jouer_action(joueur : Joueur, action : str, montant : Decimal) : None
        -distribuer_flop() : None
        -distribuer_turn() : None
        -distribuer_river() : None
        -showdown() : None
    }

    class EvaluateurMain {
        +evalue_5(cartes : List<Carte>) : (RangMain, List<int>)
        +evalue_main(privees : List<Carte>, cartes_communes : List<Carte>) : (RangMain, List<int>)
    }

    Carte *-- Valeur
    Carte *-- Couleur
    Paquet *-- Carte
    Joueur "0..2" -- "List<Carte>" Carte : cartes_privees
    Table *-- Joueur : joueurs
    Partie *-- Table
    Partie *-- Paquet
    Partie *-- Carte : cartes_communes
    EvaluateurMain ..> Carte
    EvaluateurMain ..> RangMain
    
```

```mermaid
gantt
    title Planning global – Poker Texas Hold’em
    dateFormat  YYYY-MM-DD
    section Étude préalable
      Analyse des besoins       :a1, 2025-09-15, 10d
      Cas d’utilisation        :after a1, 5d
      Diagrammes d’analyse     :5d
    section Conception générale
      Diagramme de classes     :2025-10-01, 7d
      Architecture paquetages  :7d
      Modèle physique données  :7d
    section Réalisation & Validation
      Implémentation modules   :2025-10-15, 30d
      Tests unitaires          :20d
      Tests utilisateurs       :10d
      Documentation pydoc      :10d
      Déploiement CI/CD        :15d
```



