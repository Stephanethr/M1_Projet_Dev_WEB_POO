from enum import Enum
from rpg_monstre import Monstre
from rpg_avatar import RaceType
import random

class Difficulte(Enum):
    FACILE = "Facile"
    MOYEN = "Moyenne"
    DIFFICILE = "Difficile"

class Quete:
    def __init__(self, diff: Difficulte, nvquete: int):
        self.difficulte = diff
        self.niveau_quete = nvquete
        self.monstres_a_affronter = []
        self.generer_monstres()

    def generer_monstres(self):
        if self.difficulte == Difficulte.FACILE:
            nb_monstres = random.randint(2, 3)
            niveaux = range(self.niveau_quete - 3, self.niveau_quete - 1)
        elif self.difficulte == Difficulte.MOYEN:
            nb_monstres = random.randint(3, 4)
            niveaux = range(self.niveau_quete - 1, self.niveau_quete + 2)
        else:  # Difficulte.DIFFICILE
            nb_monstres = random.randint(4, 5)
            niveaux = range(self.niveau_quete + 1, self.niveau_quete + 4)

        races_monstres = [RaceType.ORC, RaceType.LOUP_GAROU, RaceType.DEMON]

        for _ in range(nb_monstres):
            nom_monstre = f"Monstre_{random.randint(100, 999)}"
            race = random.choice(races_monstres)
            niveau = random.choice(niveaux)
            if niveau < 1:
                niveau = 1
            monstre = Monstre(nom_monstre, race, niveau)
            self.monstres_a_affronter.append(monstre)
            print(f"Monstre généré: {monstre.name} - Race: {race.value}, Niveau: {niveau}")
