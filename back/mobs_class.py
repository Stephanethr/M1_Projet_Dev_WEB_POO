from avatar_class import Avatar

class Mobs(Avatar):
    """Classe pour les mobs."""

    def __init__(self, targs):
        super().__init__(targs)
        self._type = targs["type"]

    def __str__(self):
        return f"Mobs {self._type} {self._nom}"
