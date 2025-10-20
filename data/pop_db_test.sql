INSERT INTO players (pseudo, mdp, portefeuille, code_parrainage) VALUES
('arthur', 'hash_mdp_9876', 500, 'AAA11'),
('maxence', 'hash_mdp_1234', 300, 'BBB22'),
('lucas', 'hash_mdp_5678', 800, 'CCC33'),
('clemence', 'hash_mdp_0987', 400, 'DDD44');

INSERT INTO player_stats (
    pseudo,
    meilleur_classement,
    nombre_total_mains_jouees,
    nombre_mains_jouees_session,
    nombre_all_in,
    nombre_folds,
    nombre_mises,
    nombre_relances,
    nombre_suivis,
    nombre_checks
) VALUES
('arthur', 2, 100, 15, 10, 20, 30, 10, 20, 10),
('maxence', 5, 80, 10, 5, 30, 15, 10, 20, 5),
('lucas', 1, 120, 25, 20, 25, 35, 15, 20, 5),
('clemence', 4, 90, 10, 15, 15, 20, 10, 15, 5);