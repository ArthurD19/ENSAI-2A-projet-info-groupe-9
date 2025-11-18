
# Diagramme de classes des objets métiers

Pour afficher ce diagramme dans VScode :

* à gauche aller dans **Extensions** (ou CTRL + SHIFT + X)
* rechercher `mermaid`
  * installer l'extension **Markdown Preview Mermaid Support**
* revenir sur ce fichier
  * faire **CTRL + K**, puis **V**

```mermaid
classDiagram
    %% ENUMS
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

    %% BUSINESS OBJECTS
    class Carte {
        +valeur : Valeur
        +couleur : Couleur
        +__repr__()
        +__str__()
    }

    class Deck {
        +cartes : List~Carte~
        +remplir()
        +melanger()
        +tirer() Carte
        +ajouter(carte:Carte)
        +len() int
    }

    class Joueur {
        +pseudo : str
        +solde : int
        +main : List~Carte~
        +mise : int
        +actif : bool
        +recevoir_carte(carte)
        +recevoir_du_deck(deck)
        +reset_main()
        +miser(montant)
        +suivre(montant)
        +se_coucher()
    }

    class Table {
        +id : int
        +joueurs : List~Joueur~
        +blind : int
        +pot : int
        +indice_dealer : int
        +deck : Deck
        +board : List~Carte~
        +ajouter_joueur(joueur)
        +supprimer_joueur(joueur)
        +reset_table()
    }

    class Distrib {
        +joueurs : List~Joueur~
        +deck : Deck
        +flop : List~Carte~
        +turn : Carte
        +river : Carte
        +tour_actuel : str
        +distribuer_mains()
        +distribuer_flop()
        +distribuer_turn()
        +distribuer_river()
    }

    class Comptage {
        +pot : int
        +pots_perso : dict
        +ajouter_pot_perso(joueur, montant)
        +ajouter_pot()
    }

    class ResultatMain {
        +combinaison : RangMain
        +tiebreaker_cards : List~Valeur~
        +value : int
    }

    class EvaluateurMain {
        +cartes : List~Carte~
        +evalue_main() ResultatMain
        +comparer_mains(r1, r2) int
    }

    %% ETAT / PARTIE
    class EtatPartie {
        +id_partie : int
        +tour_actuel : str
        +joueurs : list~dict~
        +board : list~str~
        +pot : int
        +pots_secondaires : dict
        +mise_max : int
        +joueur_courant : str
        +finie : bool
        +resultats : list~dict~
        +rejouer : dict
        +liste_attente : list~dict~
    }

    class Partie {
        -GROSSE_BLIND : int
        +id : int
        +table : Table
        +distrib : Distrib
        +comptage : Comptage
        +tour_actuel : str
        +mise_max : int
        +indice_joueur_courant : int
        +etat : EtatPartie
        +joueurs_ayant_joue : dict

        +initialiser_blinds()
        +passer_tour()
        +actions_joueur(pseudo, action, montant)
        +annoncer_resultats() EtatPartie
        +gestion_rejouer() bool
        +integrer_attente()
        +ajouter_a_liste_attente(joueur)
        +reponse_rejouer(pseudo, veut)
    }

    %% RELATIONS
    Carte *-- Valeur
    Carte *-- Couleur
    Deck *-- Carte
    Joueur "0..2" *-- Carte
    Table *-- Joueur
    Table *-- Deck
    Table *-- Carte : board
    Distrib *-- Deck
    Distrib *-- Joueur
    Distrib *-- Carte

    Partie *-- Table
    Partie *-- Distrib
    Partie *-- Comptage
    Partie *-- EtatPartie
    Partie *-- EvaluateurMain

    Comptage *-- Joueur

    EvaluateurMain *-- Carte
    ResultatMain *-- RangMain
    ResultatMain *-- Valeur

```



