from rpg_avatar import Avatar, RaceType, ClassType
import random

class Humain(Avatar):
    def __init__(self, name: str, race_type: RaceType, class_type: ClassType):
        super().__init__(name, race_type, class_type)  # Appelle le constructeur de la classe parente (Personnage)

    def deplacer(self, destination: int, gain: int):
        # Déplacement égal à 1d6+niveau
        super().deplacer(destination, gain)  # Appelle la méthode deplacer de la classe parente


    def positionSouhaitee(self) -> int:
        return self.position + (self.niveau + random.randint(1, 6))

    def __str__(self) -> str:
        return f"Humain {self.nom}"
