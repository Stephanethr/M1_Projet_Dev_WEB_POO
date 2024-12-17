from rpg_quete import Quete, Difficulte
from rpg_monstre import Monstre
from rpg_combat import lancer_combat
from rpg_heros import Heros
from pla_joueur import Joueur
from pla_case import Case
from pla_obstacle import Obstacle
from rpg_objet import Equipement, Consommable
import random

class Jeu:
    NB_JOUEUR_MAX = 6
    NB_CASES = 50

    def __init__(self, titre: str, nbEtapes: int, nbObstacles: int):
        self.titre = titre
        self.listeJoueurs = []
        self.cases = [None] * Jeu.NB_CASES
        self.nbEtapes = nbEtapes
        self.nbObstacles = nbObstacles
        self.scoreMax = 0
        self.monstres = []
    
    def tousLesPersos(self):
        listePersos = []
        for joueur in self.listeJoueurs:
            listePersos.extend(joueur.liste_persos)
        return listePersos

    def genererQuete(self, difficulte: Difficulte, niveau_quete: int):
        quete = Quete(difficulte, niveau_quete)
        self.monstres = quete.monstres_a_affronter
        print(f"Quête générée avec {len(quete.monstres_a_affronter)} monstres.")

    def ajouterJoueur(self, joueur: Joueur):
        if len(self.listeJoueurs) < Jeu.NB_JOUEUR_MAX:
            self.listeJoueurs.append(joueur)
        else:
            print("Nombre maximum de joueurs atteint !")

    def initialiserCases(self):
        listeIndexObstacle = []
        for _ in range(self.nbObstacles):
            gain = random.randint(1, Jeu.NB_CASES-1)
            if gain not in listeIndexObstacle:
                obstacle = Obstacle(gain*2)
                self.cases[gain] = Case(gain, obstacle)
                listeIndexObstacle.append(gain)
        for i in range(Jeu.NB_CASES):
            if i not in listeIndexObstacle:
                self.cases[i] = Case(i)

    def ajouterMonstresPlateau(self):
        for monstre in self.monstres:
            while True:
                case_aleatoire = random.randint(10, Jeu.NB_CASES-1)
                if self.cases[case_aleatoire].estLibre():
                    monstre.position = case_aleatoire
                    self.cases[case_aleatoire].placerPersonnage(monstre)
                    break
        
    def departJoueurs(self):
        for joueur in self.tousLesPersos():
            joueur.position = 0
            joueur.points_vie_max = joueur._calculer_points_vie()
            joueur.points_vie = joueur.points_vie_max
            joueur.afficher_stats()
    
    def initialiserJeu(self, diff, nv):
        print("INITIALISATION JEU")
        self.genererQuete(diff, nv)
        self.departJoueurs()
        self.initialiserCases()
        self.ajouterMonstresPlateau()
        self.afficherCases()

    def lancerJeu(self, diff, nv):
        self.initialiserJeu(diff, nv)
        while True:
            self.jouerTour()
            if not self.continuerAJouer():
                self.afficherResultats()
                break

    def continuerAJouer(self):
        # Vérifier si le héros est mort / il a atteint la fin du plateau
        pas_tlm_mort, pas_heros_termine = False, False
        for heros in self.tousLesPersos():
            if heros.est_vivant():
                pas_tlm_mort = True
                continue
        if not self.cases[Jeu.NB_CASES-1].contientHeros():
            pas_heros_termine = True
        return (pas_tlm_mort and pas_heros_termine)
            
            
    def jouerTour(self):
        print("TOUR DE JEU")
        personnages = self.tousLesPersos() + self.monstres
        for perso in personnages:
            if not perso.est_vivant():
                continue
            if isinstance(perso, Heros):
                gestion_inventaire(perso)
            #print(perso, perso.position)
            position_souhaitee = perso.positionSouhaitee()
            position_souhaitee = min(position_souhaitee, Jeu.NB_CASES - 1)
            case_visee = self.cases[position_souhaitee]
            self.cases[perso.position].enleverPersonnage()
            #print(perso, position_souhaitee)
            if case_visee.estLibre(): # Case libre
                perso.deplacer(position_souhaitee, case_visee.gain)
                case_visee.placerPersonnage(perso)
            else: # Case pas libre
                if not case_visee.sansObstacle(): # Cas ou il y a un obstacle sur la case
                    degats = random.randint(1, 2*perso.niveau)
                    print(f"{perso.name} marche sur un obstacle ! il reçoit {degats} dégâts !")
                    if not perso.recevoir_degats(degats):
                        case_visee.enleverObstacle()
                        perso.deplacer(position_souhaitee, case_visee.gain)
                        case_visee.placerPersonnage(perso)
                    else:
                       print(f"{perso.name} meurt de ses blessures sur l'obstacle !") 
                elif not isinstance(perso, case_visee.typePerso()): # Cas ou il y a un ennemi -> combat
                    if lancer_combat(perso, case_visee.perso):
                        if isinstance(perso, Heros): # perso Heros, gagne le combat
                            case_visee.enleverPersonnage()
                            perso.deplacer(position_souhaitee, case_visee.gain)
                            case_visee.placerPersonnage(perso)
                        else: # perso Monstre, perd le combat
                            pass
                    else:
                        if isinstance(perso, Heros): # perso Heros, perd le combat
                            pass
                        else: # perso Monstre, gagne le combat
                            case_visee.enleverPersonnage()
                            perso.deplacer(position_souhaitee, case_visee.gain)
                            case_visee.placerPersonnage(perso)
                else: # Il y a un allié, il reste sur sa case
                    print("La case est déjà occupée par un allié, il reste dessus !")
                    self.cases[perso.position].placerPersonnage(perso)


    def afficherCases(self):
        for i, case in enumerate(self.cases):
            if case.sansPerso() and case.sansObstacle():
                print(f"Case {i} : Libre (gain = {case.gain})")
            elif not case.sansObstacle():
                print(f"Case {i} : Obstacle (penalite = {-case.getPenalite()})")
            else:
                print(f"Case {i} : {case.perso} (penalite = {-case.gain})")

    def afficherParticipants(self):
        print("\nLISTE DES JOUEURS\n" + "-" * 25)
        for joueur in self.listeJoueurs:
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

def gestion_inventaire(personnage):
    while True:
        print(f"\nGestion de l'inventaire de {personnage.name}")
        print("0. Consulter les statistiques")
        print("1. Consulter l'inventaire")
        print("2. Équiper un objet")
        print("3. Déséquiper un objet")
        print("4. Consommer un objet")
        print("5. Terminer (par défaut)")

        choix = input("Votre choix : ") or "5"

        match choix:
            case "0":
                personnage.afficher_stats()

            case "1":
                if personnage.inventaire:
                    print("\nInventaire :")
                    for i, obj in enumerate(personnage.inventaire):
                        print(f"{i + 1}. {obj}")
                else:
                    print("\nInventaire vide.")

            case "2":
                if personnage.inventaire:
                    for i, obj in enumerate(personnage.inventaire):
                        if isinstance(obj, Equipement) and not obj.est_equipe():
                            print(f"{i + 1}. {obj}")
                    index = int(input("Choisissez un objet à équiper : ")) - 1
                    if 0 <= index < len(personnage.inventaire):
                        personnage.equiper_objet(personnage.inventaire[index])
                else:
                    print("Aucun équipement disponible.")

            case "3":
                equipe = [obj for obj in personnage.inventaire if isinstance(obj, Equipement) and obj.est_equipe()]
                if equipe:
                    for i, obj in enumerate(equipe):
                        print(f"{i + 1}. {obj}")
                    index = int(input("Choisissez un objet à déséquiper : ")) - 1
                    if 0 <= index < len(equipe):
                        personnage.desequiper_objet(equipe[index])
                else:
                    print("Aucun objet équipé.")

            case "4":
                consommables = [obj for obj in personnage.inventaire if isinstance(obj, Consommable)]
                if consommables:
                    for i, obj in enumerate(consommables):
                        print(f"{i + 1}. {obj}")
                    index = int(input("Choisissez un objet à consommer : ")) - 1
                    if 0 <= index < len(consommables):
                        personnage.consommer_objet(consommables[index])
                else:
                    print("Aucun consommable disponible.")

            case "5":
                break

            case _:
                print("Choix invalide. Veuillez réessayer.")