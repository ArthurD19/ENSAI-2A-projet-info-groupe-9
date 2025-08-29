
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
    class Joueur {
        +id: int
        +pseudo: string
        +password: string
        +solde: float
        +stats: JoueurStats
        +rejoindre_table(Table)
        +quitter_table()
        +jouer_action(str)
    }

    class Table {
        +id: int
        +joueurs: list[Joueur]
        +max_joueurs: int
        +pot: float
        +parties: list[Partie]
        +ajouter_joueur(Joueur)
        +retirer_joueur(Joueur)
        +commencer_partie()
    }

    class Partie {
        +id: int
        +deck: Deck
        +cartes_table: list[Carte]
        +mains: dict[Joueur, list[Carte]]
        +pot: float
        +tour_actuel: Joueur
        +status: string
        +distribuer_cartes()
        +jouer_tour(Joueur, str)
        +calculer_gagnant()
        +cloturer_partie()
    }

    class Deck {
        +cartes: list[Carte]
        +melanger()
        +tirer(n:int): list[Carte]
    }

    class Carte {
        +couleur: string
        +valeur: string
    }

    class Admin {
        +pseudo: string
        +crediter_joueur(Joueur, float)
        +reset_table(Table)
    }

    class PartieResult {
        +joueur: Joueur
        +gain: float
        +resultat: string
    }

    %% Relations
    Joueur --> Table : "rejoint"
    Table --> Partie : "contient"
    Partie --> Deck
    Partie --> Carte : "utilise"
    Partie --> Joueur : "implique"
    Admin --> Joueur : "gère"
    PartieResult --> Joueur

```
