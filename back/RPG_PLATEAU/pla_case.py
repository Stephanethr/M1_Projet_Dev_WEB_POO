from rpg_avatar import Avatar
from pla_obstacle import Obstacle
from rpg_heros import Heros
from rpg_monstre import Monstre

class Case:
    def __init__(self, gain: int, obs:Obstacle=None):
        self.gain = gain  # Points à ajouter ou à retirer
        self.perso = None  # Avatar présent sur la case, initialisé à None
        self.obs = obs  # Obstacle présent sur la case, initialisé avec le paramètre obs

    def getPenalite(self) -> int:
        return self.obs.get_penalite() if self.obs else 0

    def placerPersonnage(self, perso:Avatar):
        self.perso = perso

    def placerObstacle(self, obs:Obstacle):
        self.obs = obs

    def enleverObstacle(self):
        self.obs = None

    def enleverPersonnage(self):
        self.perso = None

    def estLibre(self) -> bool:
        return self.perso is None and self.obs is None

    def sansObstacle(self) -> bool:
        return self.obs is None

    def sansPerso(self) -> bool:
        return self.perso is None
    
    def contientHeros(self) -> bool:
        return self.typePerso()==Heros
    
    def typePerso(self):
        return self.perso.__class__

    def __str__(self) -> str:
        if self.estLibre():
            return f"Libre (gain = {self.gain})"
        elif self.obs:
            return f"Obstacle (pénalité = -{self.obs._penalite})"
        elif self.perso:
            return f"{self.perso.__class__.__name__} {self.perso.name} (pénalité = -{self.gain})"
        return "Erreur dans l'état de la case"
