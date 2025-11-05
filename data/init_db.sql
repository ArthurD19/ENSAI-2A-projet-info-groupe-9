-- Supprime les tables si elles existent déjà (utile pour réinitialiser la base)
DROP TABLE IF EXISTS joueurs CASCADE;
DROP TABLE IF EXISTS joueurs_statistiques CASCADE;
DROP TABLE IF EXISTS table_joueurs CASCADE;


-- Table des joueurs (infos administratives)
CREATE TABLE joueurs (
    pseudo VARCHAR(50) PRIMARY KEY,
    mdp TEXT NOT NULL,
    portefeuille INT,
    code_parrainage VARCHAR(5) UNIQUE
);

-- Table des statistiques
CREATE TABLE joueurs_statistiques (
    pseudo VARCHAR(50) PRIMARY KEY,
    meilleur_classement INT,
    nombre_total_mains_jouees INT DEFAULT 0,
    nombre_mains_jouees_session INT DEFAULT 0,
    nombre_all_in INT DEFAULT 0,
    nombre_folds INT DEFAULT 0,
    nombre_mises INT DEFAULT 0,
    nombre_relances INT DEFAULT 0,
    nombre_suivis INT DEFAULT 0,
    nombre_checks INT DEFAULT 0,
    nombre_victoire_abattage INT DEFAULT 0,
    nombre_fois_abattage INT DEFAULT 0,
    nombre_parties_dernier_mois INT DEFAULT 0,
    FOREIGN KEY (pseudo) REFERENCES joueurs(pseudo) ON DELETE CASCADE
);

-- Table qui retient les joueurs présents à chaque table
CREATE TABLE table_joueurs (
    id INTEGER PRIMARY KEY,
    joueur1 VARCHAR REFERENCES joueurs(pseudo) ON DELETE CASCADE,
    joueur2 VARCHAR REFERENCES joueurs(pseudo) ON DELETE CASCADE,
    joueur3 VARCHAR REFERENCES joueurs(pseudo) ON DELETE CASCADE,
    joueur4 VARCHAR REFERENCES joueurs(pseudo) ON DELETE CASCADE,
    joueur5 VARCHAR REFERENCES joueurs(pseudo) ON DELETE CASCADE
);

