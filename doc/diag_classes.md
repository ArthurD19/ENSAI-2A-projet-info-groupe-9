
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
        +__repr__()
        +__str__()
    }

    class Deck {
        +cartes
        +remplir()
        +melanger()
        +tirer()
        +ajouter()
        +len()
    }

    class Joueur {
        +pseudo
        +solde
        +main
        +mise
        +miser()
        +suivre()
        +se_coucher()
    }

    class Table {
        +id
        +joueurs
        +blind
        +pot
        +indice_dealer
        +paquet
        +ajouter_joueur()
        +supprimer_joueur()
    }

    class Partie {
        +démarrer_tour()
    }

    class distrib {
        +pre_flop()
        +flop()
        +turn()
        +river()
        +fin()
    }

    class Comptage {
        +pot
        +pot_perso
        +ajouter_pot()
        +ajouter_pot_perso()
        +distrib_pots()
    }

    class EvaluateurMain {
        +evalue_main()
        +comparer_mains()
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



