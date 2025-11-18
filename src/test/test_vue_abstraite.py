import pytest
from src.view.vue_abstraite import VueAbstraite


# Sous-classe factice pour tester VueAbstraite
class VueTest(VueAbstraite):
    def choisir_menu(self):
        return "menu choisi"


def test_instanciation_vue():
    vue = VueTest(message="Hello")
    assert vue.message == "Hello"
    assert isinstance(vue, VueAbstraite)


def test_afficher_affiche_message(capsys):
    vue = VueTest(message="Test Message")
    vue.afficher()
    captured = capsys.readouterr()
    assert "Test Message" in captured.out
    # Vérifie qu'il y a bien des lignes vides (simule nettoyage)
    assert captured.out.count("\n") >= 30


def test_choisir_menu_impl():
    vue = VueTest()
    assert vue.choisir_menu() == "menu choisi"

def test_choisir_menu_abstraite():
    with pytest.raises(TypeError) as excinfo:
        VueAbstraite()
    assert "Can't instantiate abstract class" in str(excinfo.value)
