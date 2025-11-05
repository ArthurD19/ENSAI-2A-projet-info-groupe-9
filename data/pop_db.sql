INSERT INTO joueurs_statistiques (
    pseudo,
    meilleur_classement,
    nombre_total_mains_jouees,
    nombre_mains_jouees_session,
    nombre_all_in,
    nombre_folds,
    nombre_mises,
    nombre_relances,
    nombre_suivis,
    nombre_checks,
    nombre_victoire_abattage,
    nombre_fois_abattage,
    nombre_parties_dernier_mois
)
VALUES
(
    'arthur1',
    3,      -- meilleur_classement
    250,    -- nombre_total_mains_jouees
    12,     -- nombre_mains_jouees_session
    15,     -- nombre_all_in
    60,     -- nombre_folds
    120,    -- nombre_mises
    40,     -- nombre_relances
    180,    -- nombre_suivis
    30,     -- nombre_checks
    10,     -- nombre_victoire_abattage
    20,     -- nombre_fois_abattage
    8       -- nombre_parties_dernier_mois
)
ON CONFLICT (pseudo) DO UPDATE
SET
    meilleur_classement = EXCLUDED.meilleur_classement,
    nombre_total_mains_jouees = EXCLUDED.nombre_total_mains_jouees,
    nombre_mains_jouees_session = EXCLUDED.nombre_mains_jouees_session,
    nombre_all_in = EXCLUDED.nombre_all_in,
    nombre_folds = EXCLUDED.nombre_folds,
    nombre_mises = EXCLUDED.nombre_mises,
    nombre_relances = EXCLUDED.nombre_relances,
    nombre_suivis = EXCLUDED.nombre_suivis,
    nombre_checks = EXCLUDED.nombre_checks,
    nombre_victoire_abattage = EXCLUDED.nombre_victoire_abattage,
    nombre_fois_abattage = EXCLUDED.nombre_fois_abattage,
    nombre_parties_dernier_mois = EXCLUDED.nombre_parties_dernier_mois;


INSERT INTO table_joueurs (id, joueur1, joueur2, joueur3, joueur4, joueur5) VALUES
(1, NULL, NULL, NULL, NULL, NULL),
(2, NULL, NULL, NULL, NULL, NULL),
(3, NULL, NULL, NULL, NULL, NULL),
(4, NULL, NULL, NULL, NULL, NULL),
(5, NULL, NULL, NULL, NULL, NULL),
(6, NULL, NULL, NULL, NULL, NULL),
(7, NULL, NULL, NULL, NULL, NULL),
(8, NULL, NULL, NULL, NULL, NULL),
(9, NULL, NULL, NULL, NULL, NULL),
(10, NULL, NULL, NULL, NULL, NULL);