class Obstacle:
    def __init__(self, penalite: int):
        self._penalite = penalite

    def get_penalite(self) -> int:
        return self._penalite
