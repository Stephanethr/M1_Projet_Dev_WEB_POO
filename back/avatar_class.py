from back.stat_class import Stat
import math
import random


class Avatar:
    """Classe générale pour un avatar."""
    id = 0

    def __init__(self, targs):
        self._nom = targs['name']
        self._race = targs['race']
        self._classe = targs['classe']
        self._bag = targs['bag']
        self._equipment = targs['equipment']
        self._element = targs['element']
        self._lvl = 1
        self._stat = Stat({'strength': 1, 'magic': 1, 'agility': 1, 'speed': 1, 'charisma': 0, 'chance': 0})
        Avatar.id += 1
        self.sumStat()
        self._life = self._stat.life_point

    def getBag(self):
        return self._bag._lItems

    def initiative(self):
        min_val = self._stat.speed
        max_val = self._stat.agility + self._stat.chance + self._stat.speed
        return random.randint(min_val, max_val)

    def damages(self):
        critique = random.randint(0, self._stat.chance)
        min_val = 0
        max_val = self._stat.attack
        if critique > self._stat.chance / 2:
            print("Full damages")
            max_dam = random.randint(max_val, 2 * max_val)
        else:
            max_dam = random.randint(min_val, max_val)
        print(f"{self._nom} dealt {max_dam} damage")
        return max_dam

    def defense(self, v):
        min_val = self._stat.agility
        max_val = self._stat.agility + self._stat.chance + self._stat.speed
        dodge = random.randint(min_val, max_val)
        damage = 0
        if dodge == max_val:
            print("The shot is dodged!")
        elif dodge > max_val / 2:
            print("Partial dodge")
            damage /= 2
        else:
            damage = v
        damage -= self._stat.defense
        damage = max(damage, 0)
        if damage > self._life:
            self._life = 0
            print("You are dead.")
        else:
            self._life -= damage
        print(f"Life points: {self._life} / {self._stat.life_point}")

    def __str__(self):
        return str(self._nom)

    def sumStat(self):
        """Additionne les statistiques de race, de classe et d'équipement."""
        equipment_bonus = 0
        for stat in self._stat.__dict__:
            for eq in self._equipment:
                equipment_bonus += eq._stat.__dict__[stat]
            self._stat.__dict__[stat] = self._race._stat.__dict__[stat] + self._classe._stat.__dict__[
                stat] + equipment_bonus

