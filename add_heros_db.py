import sqlite3
from back.RPG_DATABASE.heros_db import HerosDb
from back.RPG_PLATEAU.rpg_heros import Heros, RaceType, ClassType


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
        hero_db.save()
        print(f"Héros ajouté : {hero.name} (Niveau {hero.niveau}, Classe {hero.classe.value}, Race {hero.race.value})")

    conn.close()

if __name__ == '__main__':
    add_heroes_for_user(1)
