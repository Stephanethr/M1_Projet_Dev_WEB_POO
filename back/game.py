from bag_class import Bag
from equipment_class import Equipment
from hero_class import Hero
from item_class import Item
from mobs_class import Mobs
from quest_class import Quest
from race_class import Race
from stat_class import Stat
from json_functions import save_to_json, hero_to_dict, mob_to_dict


def game():
    ### Initialisation des races, classes, objets, héros, et mobs
    statElfe = Stat({'strength': 5, 'magic': 10, 'agility': 10, 'speed': 5, 'charisma': 5, 'chance': 5})
    elfe = Race('Elfe', statElfe)
    statHuman = Stat({'strength': 10, 'magic': 10, 'agility': 5, 'speed': 5, 'charisma': 5, 'chance': 5})
    human = Race('Human', statHuman)

    # Création des équipements
    statSword = Stat({'strength': 5, 'magic': 0, 'agility': 5, 'speed': 5, 'charisma': 0, 'chance': 5})
    sword = Equipment({'classList': 'warrior', 'place': 'hand', 'name': 'dragon sword', 'type': 'sword', 'space': 2}, statSword)

    statBaton = Stat({'strength': 0, 'magic': 10, 'agility': 0, 'speed': 5, 'charisma': 0, 'chance': 5})
    baton = Equipment({'classList': 'wizard', 'place': 'hand', 'name': 'wizard baton', 'type': 'baton', 'space': 2}, statBaton)

    statPotion = Stat({'strength': 0, 'magic': 0, 'agility': 0, 'speed': 0, 'charisma': 0, 'chance': 0})
    potion = Item({'name': 'life potion', 'type': 'potion', 'space': 2}, statPotion)

    # Création du sac d'inventaire
    myBag = Bag({"sizeMax": 20, "items": [potion, potion]})

    # Création des héros
    hero1 = Hero({'name': 'Jean', 'race': elfe, 'classe': Race('Wizard', Stat({})), 'bag': myBag, 'equipment': [baton], 'element': 'Fire', 'profession': 'chomeur'})
    hero2 = Hero({'name': 'Pierre', 'race': human, 'classe': Race('Warrior', Stat({})), 'bag': myBag, 'equipment': [sword], 'element': 'Fire', 'profession': 'chomeur'})

    # Sauvegarde des héros en JSON
    save_to_json(hero_to_dict(hero1), 'hero_jean.json')
    save_to_json(hero_to_dict(hero2), 'hero_pierre.json')

    # Création des ennemis
    mechant1 = Mobs({'name': 'orc 1', 'race': elfe, 'classe': Race('Warrior', Stat({})), 'bag': myBag, 'equipment': [sword], 'element': 'Fire', 'type': 'soldier'})

    # Sauvegarde des mobs en JSON
    save_to_json(mob_to_dict(mechant1), 'mob_orc1.json')

    # Création d'une quête
    firstQuest = Quest({'lAvatar': [mechant1], 'lvl': 2, 'gift': sword})
    print(firstQuest.run(hero1))

if __name__ == "__main__":
    game()
