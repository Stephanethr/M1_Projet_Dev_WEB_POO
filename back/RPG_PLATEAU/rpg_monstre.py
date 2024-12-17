from rpg_avatar import Avatar, RaceType, ClassType
import math, random

class Monstre(Avatar):
    """Classe spécifique pour les monstres contrôlés par le jeu"""
    def __init__(self, name: str, race_type: RaceType, niveau: int = 1):
        # Vérifie que la race est valide pour un monstre
        if race_type not in [RaceType.ORC, RaceType.LOUP_GAROU, RaceType.DEMON]:
            raise ValueError("Race non valide pour un monstre")
        super().__init__(name, race_type, ClassType.MONSTRE)
        self.niveau = niveau
        self.position = 0

        # Augmente les stats en fonction du niveau
        self._ajuster_stats_niveau()

    def positionSouhaitee(self) -> int:
        # On le fait reculer pour qu'il se rapproche du joueur
        nvlle_position = self.position
        if self.niveau//2 < 2:
            nvlle_position -= 1
        else:
            nvlle_position -= random.randint(1, self.niveau//2)
        if nvlle_position < 0:
            return 0
        else:
            return nvlle_position

    def _ajuster_stats_niveau(self):
        """Ajuste les statistiques en fonction du niveau du monstre"""
        multiplicateur = 1 + (self.niveau - 1) * 0.2  # +20% par niveau
        self.force = int(self.force * multiplicateur)
        self.endurance = int(self.endurance * multiplicateur)
        self.agilite = int(self.agilite * multiplicateur)
        
        # Recalcule les PV avec les nouvelles stats
        self.points_vie_max = self._calculer_points_vie()
        self.points_vie = self.points_vie_max

    def __str__(self):
        return f"{self.name}: Niveau {self.niveau} / Race {self.race}"