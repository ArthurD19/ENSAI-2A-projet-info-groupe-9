INSERT INTO joueurs (pseudo, mdp, portefeuille, code_parrainage) VALUES
('arthur', '5e5273fdb85dc5d8ed9b10759ffcde9c82936ef8333b67ccc2a3aa0be58e7b7c', 500, 'AAA11'),
('maxence', 'cebf15dd1986dd82dae11c2c36acf0b5fa4ea4996bd9116dc9c25f6c2cfdc598', 300, 'BBB22'),
('lucas', 'b0c704ea2c8cb6bafc4521b920e721472d128741706ca3224d5be983c1ee8fc9', 800, 'CCC33'),
('clemence', '4797d000dadc042a6b6d6cd6d5ac8069e56f0aa3a2e03055a31cf8ae09899700', 400, 'DDD44');

-- Les mots de passe sont : 
-- pour arthur : hash_mdp_9876
-- pour maxence : hash_mdp_1234
-- pour lucas : hash_mdp_5678
-- pour clemence : hash_mdp_0987
-- après hashage par la fonction dans utils/securite.py et sel = ""

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
    nombre_checks
) VALUES
('arthur', 2, 100, 15, 10, 20, 30, 10, 20, 10),
('maxence', 5, 80, 10, 5, 30, 15, 10, 20, 5),
('lucas', 1, 120, 25, 20, 25, 35, 15, 20, 5),
('clemence', 4, 90, 10, 15, 15, 20, 10, 15, 5);