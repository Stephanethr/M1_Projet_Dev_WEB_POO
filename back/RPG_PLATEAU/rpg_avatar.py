import math
import random
from enum import Enum
from dataclasses import dataclass
from typing import Dict
from rpg_objet import Objet, Equipement, Consommable
from abc import ABC, abstractmethod

# Enums pour les types
class RaceType(Enum):
    # Races humaines
    ELFE = "Elfe"
    NAIN = "Nain"
    HUMAIN = "Humain"

    # Races de monstres
    ORC = "Orc"
    LOUP_GAROU = "Loup-Garou"
    DEMON = "Démon"

class ClassType(Enum):
    GUERRIER = "Guerrier"
    RODEUR = "Rôdeur"
    ASSASSIN = "Assassin"

    # Classe nulle pour les monstres
    MONSTRE = "Monstre"

# Classes de base pour les bonus
@dataclass
class Bonus:
    force: int
    endurance: int
    agilite: int

# Définition des bonus raciaux
RACE_BONUS: Dict[RaceType, Bonus] = {
    # Races des Héros (Elfe, Nain, Humain)
    RaceType.ELFE: Bonus(1, 1, 4),
    RaceType.NAIN: Bonus(2, 3, 1),
    RaceType.HUMAIN: Bonus(2, 2, 2),

    # Races des Monstres (Orc, Loup-Garou, Démon)
    RaceType.ORC: Bonus(3, 2, 0),
    RaceType.LOUP_GAROU: Bonus(1, 1, 3),
    RaceType.DEMON: Bonus(1, 3, 1)
}

# Définition des bonus de classe
CLASS_BONUS: Dict[ClassType, Bonus] = {
    # Classes possibles (Guerrier, Rôdeur, Assassin)
    ClassType.GUERRIER: Bonus(2, 1, 0),
    ClassType.RODEUR: Bonus(1, 1, 1),
    ClassType.ASSASSIN: Bonus(1, 0, 2),

    # Classe monstre (Aucun Bonus)
    ClassType.MONSTRE: Bonus(0, 0, 0)
}

class Avatar(ABC):
    """Classe de base pour tous les personnages du jeu"""
    def __init__(self, name: str, race_type: RaceType, class_type: ClassType):
        # Propriétaire de l'Avatar
        self.proprietaire = None  # Initialise le propriétaire à None

        """
            Constructeur de la classe Avatar
        """
        self.name = name
        self.race = race_type
        self.classe = class_type
        
        # Stats de base
        self.force = 5
        self.endurance = 5
        self.agilite = 5
        
        # Bonus conférés par les équipements et consommables
        self.force_bonus = 0
        self.endurance_bonus = 0
        self.agilite_bonus = 0

        # Inventaire
        self.inventaire = [] # Contiendra les équipements et les consommables
        self.effets_temporaires = []

        # Applique les bonus
        self._bonus_classes_races()
        
        # Stats calculées
        self.niveau = 1
        self.points_vie_max = self._calculer_points_vie()
        self.points_vie = self.points_vie_max

    # GESTION DU PROPRIETAIRE
    def definirProprietaire(self, proprietaire):
        self.proprietaire = proprietaire

    """
        GESTION DES STATISTIQUES
    """

    def _calculer_points_vie(self) -> int:
        """Calcule les points de vie maximum"""
        return (self.force + self.force_bonus) + (2 * (self.endurance + self.endurance_bonus)) + (self.agilite + self.agilite_bonus)
    
    def _recalculer_pv(self):
        anciens_pvmax = self.points_vie_max
        self.points_vie_max = self._calculer_points_vie()
        # Le joueur gagne des pv en s'équipant, mais peut en perdre en se déséquipant
        self.points_vie += (self.points_vie_max-anciens_pvmax)
        if self.points_vie >= self.points_vie_max:
            self.points_vie = self.points_vie_max
        pass

    def _ajout_statistiques(self, effet):
        print(effet)
        for stat, bonus, in effet:
            setattr(self, stat, getattr(self, stat) + bonus)
        # Les points de vie sont systématiquement recalculé à chaque modification de statistiques
        self._recalculer_pv()
    
    def _retrait_statistiques(self, effet):
        for stat, bonus, in effet:
            setattr(self, stat, getattr(self, stat) - bonus)
        # Les points de vie sont systématiquement recalculé à chaque modification de statistiques
        self._recalculer_pv()

    def dissiper_effets_temporaires(self):
        for effet in self.effets_temporaires:
            for stat, bonus, in effet:
                if stat == "points_vie":
                    continue
                else:
                    setattr(self, stat, getattr(self, stat) - bonus)
            
    def _bonus_classes_races(self):
        """Applique les bonus raciaux et de classe"""
        race_bonus = RACE_BONUS[self.race]
        class_bonus = CLASS_BONUS[self.classe]
        
        # Ajout des bonus de classe et de races
        self.force += race_bonus.force + class_bonus.force
        self.endurance += race_bonus.endurance + class_bonus.endurance
        self.agilite += race_bonus.agilite + class_bonus.agilite

    """
        GESTION DES OBJETS
    """
    
    def equiper_objet(self, objet:Equipement):
        if objet in self.inventaire:
            objet.equipe = True
            self._ajout_statistiques(objet.effet.items())

    def desequiper_objet(self, objet:Equipement):
        if objet in self.inventaire and objet.est_equipe():
            objet.equipe = False
            self._retrait_statistiques(objet.effet.items())

    def ajouter_objet_inventaire(self, objet:Objet):
        self.inventaire.append(objet)
        if type(objet) is Equipement and objet.est_equipe():
            self.equiper_objet(objet)

    def retirer_objet_inventaire(self, objet:Objet):
        if type(objet) is Equipement:
            if objet.est_equipe():
                self.desequiper_objet(objet)
        self.inventaire.remove(objet)

    def consommer_objet(self, objet:Consommable):
        if not objet in self.inventaire:
            return
        self.effets_temporaires.append(objet.effet.items())
        self._ajout_statistiques(objet.effet.items())
        if objet.get_quantite() > 1:
            objet.quantite -= 1
        else:
            self.retirer_objet_inventaire(objet)

    """
        GESTION DES DEGATS
    """

    def calculer_degats(self) -> int:
        """Calcule les dégâts pour un coup"""
        degat_max = (2 * (self.force + self.force_bonus)) + ((self.endurance + self.endurance_bonus) // 2) + (self.agilite + self.agilite_bonus)
        degat = random.randint(1, degat_max)
        # Coup critique
        if degat == degat_max:
            degat += degat // 2
            #print(f"Coup critique! Dégâts: {degat}")
        return degat

    def est_vivant(self) -> bool:
        """Vérifie si l'avatar est encore en vie"""
        return self.points_vie > 0

    def recevoir_degats(self, degats: int):
        """Reçoit des dégâts et retourne True si l'avatar meurt"""
        self.points_vie = max(0, self.points_vie - degats)
        return not self.est_vivant()
    
    """
        GESTION DES DEPLACEMENTS
    """

    @abstractmethod
    def positionSouhaitee(self) -> int:
        pass

    def deplacer(self, destination: int, gain:int):
        self.position = destination


    """
        AFFICHER STATS
    """

    def afficher_stats(self):
        """Affiche les statistiques de base de l'avatar"""
        print(f"\nStatistiques de {self.name}")
        print(f"Race: {self.race.value}")
        print(f"Classe: {self.classe.value}")
        print(f"Niveau: {self.niveau}")
        print(f"Force: {self.force} (+{self.force_bonus})")
        print(f"Endurance: {self.endurance} (+{self.endurance_bonus})")
        print(f"Agilité: {self.agilite} (+{self.agilite_bonus})")
        print(f"Points de vie: {self.points_vie}/{self.points_vie_max}")
        print("Equipement :")
        for obj in self.inventaire:
            print(f"{obj}")