import sqlite3
from back.RPG_DATABASE.heros_db import HerosDb
from back.RPG_PLATEAU.rpg_heros import Heros, RaceType, ClassType
import random


def get_db_connection():
    conn = sqlite3.connect('game.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_heroes_for_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

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

if __name__ == '__main__':
    add_heroes_for_user(1)
