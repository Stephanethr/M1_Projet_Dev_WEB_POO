import sqlite3
from back.RPG_DATABASE.heros_db import HerosDb
from back.RPG_DATABASE.equipement_db import EquipementDb
from back.RPG_DATABASE.consommable_db import ConsommableDb
from back.RPG_PLATEAU.rpg_heros import Heros, RaceType, ClassType
from back.RPG_PLATEAU.rpg_objet import Equipement, Consommable, Raretes
import random


def get_db_connection():
    conn = sqlite3.connect('game.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_heroes_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('DELETE FROM heros;')
    cursor.execute("DELETE FROM SQLITE_SEQUENCE WHERE name='heros';")
    cursor.execute('DELETE FROM equipements')
    cursor.execute('DELETE FROM consommables')

    heroes_to_add = [
        Heros("Aragorn", RaceType.HUMAIN, ClassType.GUERRIER),
        Heros("Legolas", RaceType.ELFE, ClassType.RODEUR),
        Heros("Gimli", RaceType.NAIN, ClassType.ASSASSIN)
    ]

    for hero in heroes_to_add:
        hero.proprietaire = user_id
        hero_db = HerosDb(hero)
        if hero_db.id is None:
            hero_db.id = random.randint(1, 1000000)
            cursor.execute('''
                INSERT INTO heros (
                    nom, race, classe, niveau, experience, proprietaire,
                    force, endurance, agilite,
                    force_bonus, endurance_bonus, agilite_bonus,
                    points_vie, points_vie_max, position
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                hero_db.name, hero_db.race.value, hero_db.classe.value,
                hero_db.niveau, hero_db.experience, hero_db.proprietaire,
                hero_db.force, hero_db.endurance, hero_db.agilite,
                hero_db.force_bonus, hero_db.endurance_bonus, hero_db.agilite_bonus,
                hero_db.points_vie, hero_db.points_vie_max, hero_db.position
            ))
        print(f"Héros ajouté : {hero.name} (Niveau {hero.niveau}, Classe {hero.classe.value}, Race {hero.race.value})")

        conn.commit()
    conn.close()

def add_equipment_and_consumables_for_hero(hero_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Définir les objets à ajouter
    equipment_to_add = [
        Equipement("Épée longue", "Arme", Raretes.RARE, {"force_bonus": 5}, equipe=True),
        Equipement("Bouclier de fer", "Bouclier", Raretes.COMMUN, {"endurance_bonus": 3}),
        Equipement("Armure de cuir", "Armure", Raretes.LEGENDAIRE, {"endurance_bonus": 7}, equipe=True)
    ]

    consumables_to_add = [
        Consommable("Potion de soin", "Potion", Raretes.COMMUN, {"points_vie": 15}, quantite=3),
        Consommable("Potion de force", "Potion", Raretes.RARE, {"force_bonus": 4}, quantite=1),
        Consommable("Herbe médicinale", "Herbe", Raretes.COMMUN, {"points_vie": 5}, quantite=5)
    ]

    # Ajouter les équipements en base
    for equip in equipment_to_add:
        equip_db = EquipementDb(equip, hero_id)
        if getattr(equip_db, "id", None) is None:
            equip_db.id = random.randint(1, 1000000)
            cursor.execute('''
                INSERT INTO equipements (
                    nom, type_objet, rarete, effet, equipe, proprietaire
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                equip_db.nom, equip_db.type_objet, equip_db.rarete.value,
                str(equip_db.effet), equip_db.equipe, equip_db.proprietaire
            ))
            print(f"Équipement ajouté : {equip_db.nom} (Type: {equip_db.type_objet}, Rare: {equip_db.rarete.value})")

    # Ajouter les consommables en base
    for cons in consumables_to_add:
        cons_db = ConsommableDb(cons, hero_id)
        if getattr(cons_db, "id", None) is None:
            cons_db.id = random.randint(1, 1000000)
            cursor.execute('''
                INSERT INTO consommables (
                    nom, type_objet, rarete, effet, quantite, proprietaire
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                cons_db.nom, cons_db.type_objet, cons_db.rarete.value,
                str(cons_db.effet), cons_db.quantite, cons_db.proprietaire
            ))
            print(f"Consommable ajouté : {cons_db.nom} (Quantité: {cons_db.quantite}, Rare: {cons_db.rarete.value})")

    # Sauvegarder et fermer la connexion
    conn.commit()
    conn.close()


if __name__ == '__main__':
    add_heroes_for_user(1)
    add_equipment_and_consumables_for_hero(1)
