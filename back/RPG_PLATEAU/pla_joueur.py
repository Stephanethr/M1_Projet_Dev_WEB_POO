from pla_personnage import Personnage

class Joueur:
    # Attribut de classe pour compter le nombre de joueurs
    nb_joueurs = 0

    def __init__(self, nom: str):
        self.nom = nom
        Joueur.nb_joueurs += 1  # Incrémente le nombre total de joueurs
        self.code = f"J{Joueur.nb_joueurs}"  # Génère le code unique du joueur
        self.nb_points = 0  # Initialise le nombre de points à 0
        self.liste_persos = []  # Initialise la liste des personnages du joueur

    def ajouter_personnage(self, p: Personnage):
        if p not in self.liste_persos:  # Vérifie si le personnage n'est pas déjà dans la liste
            self.liste_persos.append(p)
            p.definirProprietaire(self)

    def modifier_points(self, nb: int):
        self.nb_points += nb
        if self.nb_points < 0:
            self.nb_points = 0  # Assure que les points restent positifs ou nuls

    def peut_jouer(self) -> bool:
        return len(self.liste_persos) > 0

    def __str__(self) -> str:
        return f"{self.code} {self.nom}({self.nb_points} points) avec {len(self.liste_persos)} personnages"
