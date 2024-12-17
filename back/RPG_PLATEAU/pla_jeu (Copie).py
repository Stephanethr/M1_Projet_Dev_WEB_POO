import random
from pla_joueur import Joueur
from rpg_avatar import Avatar
from pla_case import Case
from pla_obstacle import Obstacle

class Jeu:
    NB_JOUEUR_MAX = 6
    NB_CASES = 50

    def __init__(self, titre: str, nbEtapes: int, nbObstacles: int):
        self.titre = titre
        self.listeJoueurs = []  # Liste des joueurs inscrits au jeu
        self.cases = [None] * Jeu.NB_CASES  # Tableau de cases, initialisé avec des None
        self.nbEtapes = nbEtapes
        self.nbObstacles = nbObstacles
        self.scoreMax = 0  # Score maximum initialisé à 0

    def ajouterJoueur(self, joueur: Joueur):
        if len(self.listeJoueurs) < Jeu.NB_JOUEUR_MAX:
            self.listeJoueurs.append(joueur)
        else:
            print("Nombre maximum de joueurs atteint !")

    def tousLesPersos(self):
        persos = []
        for joueur in self.listeJoueurs:
            persos.extend(joueur.liste_persos)
        return persos

    def initialiserCases(self):
        nbObstaclesCree = 0
        for i in range(Jeu.NB_CASES):
            gain = random.randint(1, Jeu.NB_CASES)  # Gain aléatoire entre 1 et NB_CASES
            if (gain % 5) == 0 and nbObstaclesCree < self.nbObstacles:
                obstacle = Obstacle(gain * 2)  # Pénalité de l'obstacle = gain*2
                self.cases[i] = Case(gain, obstacle)
                nbObstaclesCree += 1
            else:
                self.cases[i] = Case(gain)

    def lancerJeu(self):
        personnages = self.tousLesPersos()
        self.initialiserCases()
        for etape in range(self.nbEtapes):
            for perso in personnages:
                position_souhaitee = perso.positionSouhaitee()
                if position_souhaitee >= Jeu.NB_CASES:
                    position_souhaitee = Jeu.NB_CASES - 1  # Si dépassement, atteindre la dernière case

                case_visee = self.cases[position_souhaitee]
                self.cases[perso.position].enleverPersonnage()

                if case_visee.estLibre():
                    perso.deplacer(position_souhaitee, case_visee.gain)  # Déplacement et gain
                    case_visee.placerPersonnage(perso)
                else:
                    # Case occupée : application d'une pénalité
                    if not case_visee.sansObstacle():
                        perso.penaliser(case_visee.getPenalite())  # Case occupée par un obstacle
                    else:
                        perso.penaliser(case_visee.gain)  # Case occupée par un autre personnage

        self.afficherResultats()  # Affiche les résultats à la fin de toutes les étapes

    def afficherCases(self):
        for i, case in enumerate(self.cases):
            if case.sansPerso() and case.sansObstacle():
                print(f"Case {i} : Libre (gain = {case.gain})")
            elif not case.sansObstacle():
                print(f"Case {i} : Obstacle (penalite = {-case.getPenalite()})")
            else:
                print(f"Case {i} : {case.perso} (penalite = {-case.gain})")

    def afficherParticipants(self):
        print("LISTE DES JOUEURS\n" + "-" * 25)
        for joueur in self.listeJoueurs:
            print("LISTE DES JOUEURS\n" + "-" * 25)
            print(joueur)

    def afficherResultats(self):
        self.afficherParticipants()
        gagnant = max(self.listeJoueurs, key=lambda j: j.nb_points)
        print("\nRESULTATS")
        print(f"Le gagnant est {gagnant.nom} avec {gagnant.nb_points} points")

        # Vérifier si le score est un record
        if gagnant.nb_points > self.scoreMax:
            print(f"Record battu : Ancien score maximum {self.scoreMax}")
            self.scoreMax = gagnant.nb_points
        else:
            print(f"Score maximum reste {self.scoreMax}")

    def __str__(self):
        return f"JEU {self.titre}"
