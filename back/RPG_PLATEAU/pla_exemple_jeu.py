from pla_jeu import Jeu
from pla_joueur import Joueur
from rpg_objet import Equipement, Consommable, Raretes
from rpg_heros import Heros, RaceType, ClassType
from rpg_quete import Difficulte


# Création d'un jeu
jeu = Jeu("AtelierPOO", 10, 5)

# Ajouter des joueurs
joueur1 = Joueur("Paul")
joueur2 = Joueur("Thomas")
jeu.ajouterJoueur(joueur1)
jeu.ajouterJoueur(joueur2)

equipement1 = Equipement("Epée forte", "Arme", Raretes.COMMUN, {"force_bonus":10})
equipement2 = Equipement("Capuchon en laine", "Vêtement", Raretes.RARE, {"agilite_bonus":10}, True)
equipement3 = Equipement("Plastron en maille", "Armure", Raretes.LEGENDAIRE, {"endurance_bonus":20})

potion1 = Consommable("Potion de soin", "Potion", Raretes.COMMUN, {"points_vie":10}, 2)
potion2 = Consommable("Potion du géant", "Potion", Raretes.LEGENDAIRE, {"points_vie":20, "force_bonus":10})
potion3 = Consommable("Herbe medicinale", "Herbe", Raretes.RARE, {"points_vie":5, "endurance_bonus":1}, 10)

humain1 = Heros("Aragorn", RaceType.HUMAIN, ClassType.GUERRIER)
elfe1 = Heros("Rass'al'Ghoul", RaceType.ELFE, ClassType.RODEUR)
nain1 = Heros('issou-la-chancla', RaceType.NAIN, ClassType.ASSASSIN)

humain1.ajouter_objet_inventaire(equipement1)
humain1.ajouter_objet_inventaire(equipement2)
humain1.ajouter_objet_inventaire(potion1)
humain1.ajouter_objet_inventaire(potion2)
elfe1.ajouter_objet_inventaire(equipement3)
elfe1.ajouter_objet_inventaire(potion3)

joueur1.ajouter_personnage(nain1)
joueur1.ajouter_personnage(humain1)
joueur2.ajouter_personnage(elfe1)

jeu.lancerJeu(Difficulte.FACILE, 1)
jeu.lancerJeu(Difficulte.MOYEN, 2)
jeu.lancerJeu(Difficulte.DIFFICILE, 3)