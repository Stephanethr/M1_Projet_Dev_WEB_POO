from .rpg_avatar import Avatar, RaceType, ClassType
import math, random

MULTIPLICATEUR = 1.25

class Heros(Avatar):
    """Classe spécifique pour les héros contrôlés par le joueur"""
    def __init__(self, name: str, race_type: RaceType, class_type: ClassType):
        # Vérifie que la race et la classe sont valides pour un héros
        if race_type not in [RaceType.ELFE, RaceType.NAIN, RaceType.HUMAIN]:
            raise ValueError("Race non valide pour un héros")
        if class_type == ClassType.MONSTRE:
            raise ValueError("Un héros ne peut pas avoir la classe Monstre")
        super().__init__(name, race_type, class_type)
        self.experience = 0
        self.position = 0 # Position de base au début du plateau

    def niveau_suivant(self):
        self.niveau += 1
        # Augmentation des statistiques de 25%
        self.force = int(self.force * MULTIPLICATEUR)
        self.endurance = int(self.endurance * MULTIPLICATEUR)
        self.agilite = int(self.agilite * MULTIPLICATEUR)

        print(f"{self.name} passe au niveau {self.niveau}!")
        self._recalculer_pv()
        self.xp = 0


    def gagner_experience(self, niveau_monstre: int):
        """Gagne de l'expérience basée sur le niveau du monstre vaincu"""
        xp_gagne = 2**niveau_monstre  # XP gagné - 2**xp_gagne
        self.experience += xp_gagne
        if self.niveau < (2 * math.log(self.experience)):
            # On gagne un niveau supplémentaire
            self.niveau_suivant()
        else:
            pass
            #print(f"XP: {self.experience}")
        
        return xp_gagne
    
    def deplacer(self, destination: int, gain: int):
        super().deplacer(destination, gain)
        self.proprietaire.modifier_points(gain)

    def penaliser(self, penalite: int):
        if self.proprietaire is not None:
            self.proprietaire.modifier_points(-penalite)


    def positionSouhaitee(self) -> int:
        return self.position + (self.niveau + random.randint(1, 6))


    def afficher_stats(self):
        """Affiche les statistiques complètes du héros"""
        super().afficher_stats()

    def __str__(self):
        return f"{self.name}: Niveau {self.niveau}"