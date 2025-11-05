-- Supprime les tables si elles existent déjà (utile pour réinitialiser la base)
DROP TABLE IF EXISTS joueurs CASCADE;
DROP TABLE IF EXISTS joueurs_statistiques CASCADE;
DROP TABLE IF EXISTS table_partie CASCADE;
DROP TABLE IF EXISTS table_joueur CASCADE;


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

-- Table Partie (correspond à la table où se déroule la partie)
CREATE TABLE table_partie (
    id SERIAL PRIMARY KEY,
    blind INTEGER DEFAULT 10 CHECK (blind >= 0),
    pot INTEGER DEFAULT 0 CHECK (pot >= 0),
    indice_dealer INTEGER NOT NULL DEFAULT 0,
    deck JSONB NOT NULL,
    board JSONB NOT NULL
);

-- Table joueur fait le lien entre la table et les joueurs
CREATE TABLE table_joueur (
    table_id INTEGER REFERENCES table_partie(id) ON DELETE CASCADE,
    joueur_id INTEGER REFERENCES joueurs(id) ON DELETE CASCADE,
    PRIMARY KEY (table_id, joueur_id)
);

