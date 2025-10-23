import random
import string

from dao.joueur_dao import existe_code_parrainage
# existe_code_parrainage à coder dans DAO joueur

class GenerateurDeCode:
    def __init__(self, length=8):
        """Initialise le générateur de code avec une longueur par défaut."""
        self.length = length

    def generate_unique_code(self):
        """Génère et renvoie un code de parrainage unique."""
        while True:
            # Génère un code aléatoire (ex : 'AB3F7H2K')
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=self.length))
            
            # Vérifie via la fonction importée si le code existe déjà
            if not existe_code_parrainage(code):
                return code
