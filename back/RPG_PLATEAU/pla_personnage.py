from abc import ABC, abstractmethod
from rpg_avatar import Avatar

class Personnage(ABC):
    def __init__(self, nom: str, age: int):
        self.nom = nom
        self.age = age
        self.position = 0  # Initialise la position par défaut à 0
        self.proprietaire = None  # Initialise le propriétaire à None

    def deplacer(self, destination: int, gain: int):
        self.position = destination
        if self.proprietaire is not None:
            self.proprietaire.modifier_points(gain)

    def definirProprietaire(self, proprietaire):
        self.proprietaire = proprietaire

    def penaliser(self, penalite: int):
        if self.proprietaire is not None:
            self.proprietaire.modifier_points(-penalite)

    def __str__(self) -> str:
        return self.nom

    @abstractmethod
    def positionSouhaitee(self) -> int:
        pass
