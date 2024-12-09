from avatar_class import Avatar
import math
from datetime import date


class Hero(Avatar):
    """Classe pour les héros."""

    def __init__(self, targs):
        super().__init__(targs)
        self._xp = 1
        self._profession = targs['profession']
        self._lvl = self.lvl()

    def lvl(self):
        lvl = math.floor(self._xp / 100)
        lvl = max(lvl, 1)
        if lvl > self._lvl:
            print("### New level ###")
            self.newLvl()
        return lvl

    def newLvl(self):
        for stat in self._stat.__dict__:
            self._stat.__dict__[stat] += 5
        self._life = self._stat.life_point
        print("### Stats upgraded ###")

    def setXP(self, xp):
        self._xp += xp
        self._lvl = self.lvl()

    def __str__(self):
        return f"Joueur {self._nom} de niveau {self._lvl} classe {self._classe} race {self._race}"

    def save(self):
        fileName = f"{date.today()}_{Hero.id}_{self._nom}.txt"
        with open(fileName, "w+") as f:
            f.write(self._nom + "\n")
            f.write(self._race._name + "\n")
            f.write(self._classe._name + "\n")
            f.write(f"lvl: {self._lvl}\n")
            f.write(f"xp: {self._xp}\n")
            for stat in self._stat.__dict__:
                f.write(f"{stat} {self._stat.__dict__[stat]}\n")
            for eq in self._equipment:
                f.write(str(eq) + "\n")
            for item in self.getBag():
                f.write(str(item) + "\n")

    def saveXML(self):
        fileName = f"{date.today()}_{Hero.id}_{self._nom}.xml"
        xml = "<?xml version='1.0' encoding='UTF-8'?>"
        xml += f"<avatar id='{Hero.id}'>"
        xml += f"<name>{self._nom}</name>"
        xml += f"<race>{self._race._name}</race>"
        xml += f"<level>{self._classe._name}</level>"
        xml += f"<xp>{self._lvl}</xp>"
        xml += f"<name>{self._xp}</name>"
        xml += "<stats>"
        for stat in self._stat.__dict__:
            xml += f"<{stat}>{self._stat.__dict__[stat]}</{stat}>"
        xml += "</stats>"
        xml += "<equipments>"
        it = 1
        for eq in self._equipment:
            xml += f"<item_{it}>{eq._name}</item_{it}>"
            it += 1
        xml += "</equipments>"
        xml += "<bag>"
        it = 1
        for item in self.getBag():
            xml += f"<item_{it}>{item._name}</item_{it}>"
            it += 1
        xml += "</bag>"
        xml += "</avatar>"
        with open(fileName, "w+") as f:
            f.write(xml)

    @staticmethod
    def load():
        pass
