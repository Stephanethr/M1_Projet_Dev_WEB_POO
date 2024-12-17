import random
from pla_personnage import Personnage

class Tauren(Personnage):
    def __init__(self, nom: str, age: int, taille: int):
        super().__init__(nom, age)  # Appelle le constructeur de la classe parente (Personnage)
        self.taille = taille  # Initialise la taille du Tauren

    def positionSouhaitee(self) -> int:
        deplacement_aleatoire = random.randint(1, self.taille)  # Nombre aléatoire entre 1 et la taille
        nouveau_deplacement = self.position - deplacement_aleatoire
        return nouveau_deplacement if nouveau_deplacement > 0 else 0

    def __str__(self) -> str:
        return f"Tauren {self.nom}"
