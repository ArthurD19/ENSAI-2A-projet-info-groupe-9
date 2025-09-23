
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
    %% Enums
    class Couleur {
        <<enumeration>>
        PIQUE
        TREFLE
        CARREAU
        COEUR
    }

    class Valeur {
        <<enumeration>>
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
        <<enumeration>>
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

    %% Objets métiers
    class Carte {
        +valeur : Valeur
        +couleur : Couleur
        +__repr__() str
        +__str__() str
    }

    class Deck {
        +cartes : List~Carte~
        +remplir() None
        +melanger() None
        +tirer() Carte
        +ajouter(carte : Carte) None
        +len() int
    }

    class Joueur {
        +pseudo : str
        +solde : int
        +main : List~Carte~
        +mise : int
        +miser(montant : int) None
        +suivre() None
        +se_coucher() None
    }

    class Table {
        +id : int
        +joueurs : List~Joueur~
        +blind : int
        +pot : int
        +indice_dealer : int
        +paquet : Deck
        +board : List~Carte~
        +ajouter_joueur(joueur : Joueur) None
        +supprimer_joueur(joueur : Joueur) None
    }

    class Partie {
        +démarrer_tour() None
    }

    class distrib {
        +pre_flop(table : Table, indice_dealer : int) None
        +flop(table : Table, indice_dealer : int) None
        +turn(table : Table, indice_dealer : int) None
        +river(table : Table, indice_dealer : int) None
        +fin(table : Table) None
    }

    class Comptage {
        +pot : int
        +pots_perso : List~Dict~Joueur, int~~
        +ajouter_pot(table : Table) None
        +ajouter_pot_perso(joueur : Joueur, montant : int) None
        +distrib_pots(gagnants : List~Joueur~) Dict~Joueur, int~
    }

    class EvaluateurMain {
        +evalue_main(main : List~Carte~, board : List~Carte~) RangMain
        +comparer_mains(mains : Dict~Joueur, List~Carte~) Joueur
    }

    %% Relations / hiérarchies
    Carte *-- Valeur
    Carte *-- Couleur
    Joueur "0..2" *-- Carte
    Deck *-- Carte
    Table *-- Joueur
    Table *-- Deck
    Partie *-- distrib
    Partie *-- Comptage
    Partie *-- EvaluateurMain
    Partie ..> Table
    EvaluateurMain *-- RangMain
```




```mermaid
gantt
    title WIP Test Planning global – Poker Texas Hold’em
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
```



