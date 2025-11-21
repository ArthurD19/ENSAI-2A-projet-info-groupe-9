import pytest
from unittest.mock import patch, MagicMock
from src.service.joueur_service import JoueurService
from src.business_object.joueurs import Joueur  
from src.service.connexion_service import ConnexionService
from src.service.statistique_service import StatistiqueService
from src.service.table_service import TableService

@pytest.fixture
def service_table():
    # Réinitialiser le singleton
    TableService._instances = {}  # <-- vide le dict interne du Singleton
    # Crée un TableService avec seulement 2 tables
    return TableService(nb_tables=2, blind=20)

@pytest.fixture
def service_stat():
    return StatistiqueService()

@pytest.fixture
def service():
    return JoueurService()

def test_creer_sans_code_parrainage(service):
    with patch("service.joueur_service.JoueurDao") as mock_dao, \
         patch.object(service, "pseudo_deja_utilise", return_value=False):
        mock_instance = mock_dao.return_value
        mock_instance.creer.return_value = True
        pseudo, mdp = "TestUser", "password123"
        joueur = service.creer_sans_code_parrainage(pseudo, mdp)
        
        assert joueur["pseudo"] == pseudo
        assert joueur["portefeuille"] == 1000
        assert joueur["code_parrainage"] is None
        assert "mdp" in joueur


def test_creer_sans_code_parrainage_pseudo_trop_court(service):
    joueur = service.creer_sans_code_parrainage("ab", "password")
    assert joueur is None

def test_pseudo_deja_utilise(service):
    with patch("src.service.joueur_service.JoueurDao") as mock_dao:
        mock_dao.return_value.pseudo_existe.return_value = True
        assert service.pseudo_deja_utilise("existing") is True

def test_se_connecter_ok(service):
    with patch("service.joueur_service.JoueurDao") as mock_dao, \
         patch("service.joueur_service.Session") as mock_session, \
         patch("service.joueur_service.hash_password") as mock_hash:
        mock_hash.return_value = "hashed"
        mock_dao.return_value.se_connecter.return_value = {"pseudo": "Alice"}
        ok, joueur = service.se_connecter("Alice", "pwd")
        assert ok is True
        assert joueur["pseudo"] == "Alice"

def test_se_connecter_deja_connecte(service):
    with patch("service.joueur_service.JoueurDao") as mock_dao, \
         patch("service.joueur_service.hash_password") as mock_hash:
        mock_hash.return_value = "hashed"
        mock_dao.return_value.se_connecter.return_value = "DEJA_CONNECTE"
        ok, msg = service.se_connecter("Alice", "pwd")
        assert ok is False
        assert "déjà connecté" in msg

def test_se_connecter_mauvais_pseudo(service):
    with patch("service.joueur_service.JoueurDao") as mock_dao, \
         patch("service.joueur_service.hash_password") as mock_hash:
        mock_hash.return_value = "hashed"
        mock_dao.return_value.se_connecter.return_value = None
        ok, msg = service.se_connecter("Alice", "pwd")
        assert ok is False
        assert "Pseudo ou mot de passe invalide" in msg

def test_generer_code_parrainage_nouveau(service):
    with patch("src.service.joueur_service.JoueurDao") as mock_dao, \
         patch("src.service.joueur_service.GenerateurDeCode") as mock_gen:
        mock_dao.return_value.trouver_par_pseudo.return_value = {"pseudo": "Bob", "code_parrainage": None}
        mock_gen.return_value.generate_unique_code.return_value = "CODE123"
        mock_dao.return_value.mettre_a_jour_code_de_parrainage.return_value = True
        code = service.generer_code_parrainage("Bob")
        assert code == "CODE123"

def test_generer_code_parrainage_existant(service):
    with patch("src.service.joueur_service.JoueurDao") as mock_dao:
        mock_dao.return_value.trouver_par_pseudo.return_value = {"pseudo": "Bob", "code_parrainage": "EXIST123"}
        code = service.generer_code_parrainage("Bob")
        assert code == "EXIST123"

def test_credit_auto(service):
    with patch("src.service.joueur_service.JoueurDao") as mock_dao, \
         patch("src.service.joueur_service.logging") as mock_logging:
        mock_dao.return_value.joueurs_a_crediter.return_value = ["Alice"]
        service.credit_auto()
        mock_dao.return_value.crediter.assert_called_with("Alice", service.MONTANT_RECHARGEMENT_AUTO)
        mock_dao.return_value.maj_date_credit_auto.assert_called_with("Alice")

def test_creer_sans_code_parrainage_pseudo_existant(service):
    with patch.object(service, "pseudo_deja_utilise", return_value=True):
        joueur = service.creer_sans_code_parrainage("ExistingUser", "password")
        assert joueur is None

def test_creer_sans_code_parrainage_dao_echec(service):
    with patch("src.service.joueur_service.JoueurDao") as mock_dao, \
         patch.object(service, "pseudo_deja_utilise", return_value=False):
        mock_dao.return_value.creer.return_value = False
        joueur = service.creer_sans_code_parrainage("NewUser", "password")
        assert joueur is None

def test_credit_auto_plusieurs_joueurs(service):
    with patch("src.service.joueur_service.JoueurDao") as mock_dao, \
         patch("src.service.joueur_service.logging") as mock_logging:
        mock_dao.return_value.joueurs_a_crediter.return_value = ["Alice", "Bob"]
        service.credit_auto()
        mock_dao.return_value.crediter.assert_any_call("Alice", service.MONTANT_RECHARGEMENT_AUTO)
        mock_dao.return_value.crediter.assert_any_call("Bob", service.MONTANT_RECHARGEMENT_AUTO)
        mock_dao.return_value.maj_date_credit_auto.assert_any_call("Alice")
        mock_dao.return_value.maj_date_credit_auto.assert_any_call("Bob")

def test_generer_code_parrainage_aucun_joueur(service):
    with patch("service.joueur_service.JoueurDao") as mock_dao, \
         patch("service.joueur_service.GenerateurDeCode") as mock_gen:
        mock_dao.return_value.trouver_par_pseudo.return_value = None
        code = service.generer_code_parrainage("Inconnu")
        assert code is None

def test_generer_code_parrainage_echec_update(service):
    with patch("src.service.joueur_service.JoueurDao") as mock_dao, \
         patch("src.service.joueur_service.GenerateurDeCode") as mock_gen:
        # joueur sans code existant
        mock_dao.return_value.trouver_par_pseudo.return_value = {"pseudo": "Bob", "code_parrainage": None}
        mock_gen.return_value.generate_unique_code.return_value = "CODE123"
        # échec de la mise à jour
        mock_dao.return_value.mettre_a_jour_code_de_parrainage.return_value = False

        code = service.generer_code_parrainage("Bob")
        assert code == "code non genere"

def test_se_connecter_ok():
    service = ConnexionService()
    with patch("src.service.connexion_service.JoueurDao") as mock_dao, \
         patch("src.service.connexion_service.hash_password") as mock_hash, \
         patch("src.service.connexion_service.Session") as mock_session:

        mock_hash.return_value = "hashedpwd"
        mock_dao.return_value.se_connecter.return_value = {"pseudo": "Alice", "portefeuille": 500}

        succes, joueur = service.se_connecter("Alice", "pwd")
        assert succes is True
        assert joueur["pseudo"] == "Alice"


def test_se_connecter_deja_connecte():
    service = ConnexionService()
    with patch("src.service.connexion_service.JoueurDao") as mock_dao, \
         patch("src.service.connexion_service.hash_password") as mock_hash:

        mock_hash.return_value = "hashedpwd"
        mock_dao.return_value.se_connecter.return_value = "DEJA_CONNECTE"

        succes, message = service.se_connecter("Alice", "pwd")
        assert succes is False
        assert message == "Vous êtes déjà connecté avec ce pseudo."


def test_se_connecter_echec():
    service = ConnexionService()
    with patch("src.service.connexion_service.JoueurDao") as mock_dao, \
         patch("src.service.connexion_service.hash_password") as mock_hash:

        mock_hash.return_value = "hashedpwd"
        mock_dao.return_value.se_connecter.return_value = None

        succes, message = service.se_connecter("Alice", "pwd")
        assert succes is False
        assert message == "Pseudo ou mot de passe invalide."


def test_se_deconnecter_ok():
    service = ConnexionService()
    with patch("src.service.connexion_service.JoueurDao") as mock_dao, \
         patch("src.service.connexion_service.Session") as mock_session:

        mock_dao.return_value.deconnecter.return_value = True
        result = service.se_deconnecter("Alice")
        assert result is True


def test_se_deconnecter_echec():
    service = ConnexionService()
    with patch("src.service.connexion_service.JoueurDao") as mock_dao, \
         patch("src.service.connexion_service.Session") as mock_session:

        mock_dao.return_value.deconnecter.return_value = False
        result = service.se_deconnecter("Alice")
        assert result is False

def test_afficher_statistiques_joueur_ok(service_stat):
    with patch("src.service.statistique_service.StatistiqueDao") as mock_dao:
        mock_dao.return_value.trouver_statistiques_par_id.return_value = {
            "pseudo": "Alice",
            "parties_gagnees": 10,
            "parties_perdues": 5
        }
        stats = service_stat.afficher_statistiques_joueur("Alice")
        assert stats["pseudo"] == "Alice"
        assert stats["parties_gagnees"] == 10
        assert stats["parties_perdues"] == 5


def test_afficher_statistiques_joueur_aucune_stat(service_stat):
    with patch("src.service.statistique_service.StatistiqueDao") as mock_dao:
        mock_dao.return_value.trouver_statistiques_par_id.return_value = None
        stats = service_stat.afficher_statistiques_joueur("Inconnu")
        assert stats is None

def test_get_table_existe(service_table):
    table = service_table.get_table(1)
    assert table is not None
    assert table.id == 1

def test_get_table_inexistante(service_table):
    table = service_table.get_table(999)
    assert table is None

def test_rejoindre_table_ok(service_table):
    with patch("src.service.table_service.JoueurDao") as mock_dao, \
         patch("src.service.table_service.PartieService") as mock_partie_service:

        mock_dao.return_value.valeur_portefeuille.return_value = 1000
        mock_partie_service.return_value.rejoindre_partie.return_value = (True, "EN_COURS", "Joueur ajouté")

        success, etat, msg = service_table.rejoindre_table("Alice", 1)
        assert success is True
        assert etat == "EN_COURS"
        assert "Joueur ajouté" in msg

def test_rejoindre_table_deja_present(service_table):
    with patch("src.service.table_service.JoueurDao") as mock_dao, \
         patch("src.service.table_service.PartieService") as mock_partie_service:

        mock_dao.return_value.valeur_portefeuille.return_value = 1000
        mock_partie_service.return_value.rejoindre_partie.return_value = (True, "EN_COURS", "Joueur ajouté")

        # Premier ajout
        service_table.rejoindre_table("Alice", 1)
        # Deuxième ajout du même joueur
        success, etat, msg = service_table.rejoindre_table("Alice", 1)
        assert success is False
        assert "déjà à la table" in msg

def test_rejoindre_table_inexistante(service_table):
    success, etat, msg = service_table.rejoindre_table("Bob", 999)
    assert success is False
    assert etat is None
    assert "n'existe pas" in msg

def test_quitter_table_ok(service_table):
    with patch("src.service.table_service.JoueurDao") as mock_dao, \
         patch("src.service.table_service.PartieService") as mock_partie_service:

        mock_dao.return_value.valeur_portefeuille.return_value = 1000
        mock_partie_service.return_value.rejoindre_partie.return_value = (True, "EN_COURS", "Joueur ajouté")

        service_table.rejoindre_table("Alice", 1)
        result = service_table.quitter_table("Alice", 1)
        assert result == 1
        # Vérifie que le joueur n'est plus dans la table
        table = service_table.get_table(1)
        assert all(j.pseudo != "Alice" for j in table.joueurs)

def test_quitter_table_inexistante(service_table):
    result = service_table.quitter_table("Alice", 999)
    assert result == 2

def test_lister_tables(service_table):
    tables = service_table.lister_tables()
    assert len(tables) == 2
    assert all("id" in t and "nb_joueurs" in t and "blind" in t for t in tables)

def test_etat_tables(service_table):
    etat = service_table.etat_tables()
    assert len(etat) == 2
    assert all("table" in t and "blind" in t and "joueurs" in t for t in etat)

def test_get_table(service_table):
    table = service_table.get_table(1)
    assert table is not None
    assert table.id == 1

def test_quitter_table(service_table):
    pseudo = "Alice"
    # Assurer que le joueur est présent
    service_table.tables[1].joueurs.append(Joueur(pseudo, 1000))
    code = service_table.quitter_table(pseudo, 1)
    assert code == 1
    assert pseudo not in [j.pseudo for j in service_table.tables[1].joueurs]

def test_rejoindre_table(service_table):
    with patch("src.dao.joueur_dao.JoueurDao.valeur_portefeuille", return_value=2000):
        success, etat, msg = service_table.rejoindre_table("Alice", 1)
    assert success is True
    assert "Alice" in [j.pseudo for j in service_table.tables[1].joueurs]

def test_se_connecter():
    service_connexion = ConnexionService()

    with patch("src.service.connexion_service.JoueurDao.se_connecter", return_value={"pseudo": "Alice"}), \
         patch("src.service.connexion_service.hash_password", return_value="hashed"), \
         patch("src.service.connexion_service.Session.connexion", return_value=None):

        success, joueur = service_connexion.se_connecter("Alice", "pwd")

        # Vérifier que la connexion a réussi
        assert success is True
        assert joueur["pseudo"] == "Alice"