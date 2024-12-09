import json_functions

def save_to_json(data, filename):
    """Sauvegarde des données dans un fichier JSON."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def load_from_json(filename):
    """Charge des données depuis un fichier JSON."""
    with open(filename, 'r') as file:
        return json.load(file)

def hero_to_dict(hero):
    """Convertit un objet Hero en dictionnaire pour le sauvegarder en JSON."""
    return {
        'name': hero.name,
        'race': hero.race.name,
        'class': hero.classe.name,
        'bag': [item_to_dict(item) for item in hero.bag.items],
        'equipment': [equipment_to_dict(equip) for equip in hero.equipment],
        'element': hero.element,
        'profession': hero.profession,
        'life_points': hero.life_points
    }

def item_to_dict(item):
    """Convertit un objet Item en dictionnaire."""
    return {
        'name': item.name,
        'type': item.type,
        'stats': item.stats.stats
    }

def equipment_to_dict(equip):
    """Convertit un objet Equipment en dictionnaire."""
    return {
        'name': equip.name,
        'type': equip.type,
        'place': equip.place,
        'stats': equip.stats.stats
    }

def mob_to_dict(mob):
    """Convertit un objet Mobs en dictionnaire."""
    return {
        'name': mob.name,
        'race': mob.race.name,
        'class': mob.classe.name,
        'life_points': mob.life_points,
        'equipment': [equipment_to_dict(equip) for equip in mob.equipment],
        'bag': [item_to_dict(item) for item in mob.bag.items],
        'element': mob.element,
        'type': mob.type
    }
