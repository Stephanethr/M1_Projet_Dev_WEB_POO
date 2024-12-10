from back.avatar_class import Avatar
import math
from datetime import date

from init_db import get_db_connection


class Hero(Avatar):
    """Classe pour les héros."""

    def __init__(self, targs):
        super().__init__(targs)
        self._xp = 1
        self._profession = targs['profession']
        self._lvl = self.lvl()

    def lvl(self):
        lvl = math.floor(self._xp / 100)
        lvl = max(lvl, 1)
        if lvl > self._lvl:
            print("### New level ###")
            self.newLvl()
        return lvl

    def newLvl(self):
        for stat in self._stat.__dict__:
            self._stat.__dict__[stat] += 5
        self._life = self._stat.life_point
        print("### Stats upgraded ###")

    def setXP(self, xp):
        self._xp += xp
        self._lvl = self.lvl()

    def __str__(self):
        return f"Joueur {self._nom} de niveau {self._lvl} classe {self._classe} race {self._race}"

    def save(self):
        fileName = f"{date.today()}_{Hero.id}_{self._nom}.txt"
        with open(fileName, "w+") as f:
            f.write(self._nom + "\n")
            f.write(self._race._name + "\n")
            f.write(self._classe._name + "\n")
            f.write(f"lvl: {self._lvl}\n")
            f.write(f"xp: {self._xp}\n")
            for stat in self._stat.__dict__:
                f.write(f"{stat} {self._stat.__dict__[stat]}\n")
            for eq in self._equipment:
                f.write(str(eq) + "\n")
            for item in self.getBag():
                f.write(str(item) + "\n")

    def saveXML(self):
        fileName = f"{date.today()}_{Hero.id}_{self._nom}.xml"
        xml = "<?xml version='1.0' encoding='UTF-8'?>"
        xml += f"<avatar id='{Hero.id}'>"
        xml += f"<name>{self._nom}</name>"
        xml += f"<race>{self._race._name}</race>"
        xml += f"<level>{self._classe._name}</level>"
        xml += f"<xp>{self._lvl}</xp>"
        xml += f"<name>{self._xp}</name>"
        xml += "<stats>"
        for stat in self._stat.__dict__:
            xml += f"<{stat}>{self._stat.__dict__[stat]}</{stat}>"
        xml += "</stats>"
        xml += "<equipments>"
        it = 1
        for eq in self._equipment:
            xml += f"<item_{it}>{eq._name}</item_{it}>"
            it += 1
        xml += "</equipments>"
        xml += "<bag>"
        it = 1
        for item in self.getBag():
            xml += f"<item_{it}>{item._name}</item_{it}>"
            it += 1
        xml += "</bag>"
        xml += "</avatar>"
        with open(fileName, "w+") as f:
            f.write(xml)

    def saveBDD(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Enregistrement du héros dans la table heroes
            cursor.execute('''
                INSERT INTO heroes (id, name, race, classe, level, xp, user_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    race = excluded.race,
                    classe = excluded.classe,
                    level = excluded.level,
                    xp = excluded.xp,
                    user_id = excluded.user_id
            ''', (Hero.id, self._nom, self._race._name, self._classe._name, self._lvl, self._xp, self._user_id))

            # Enregistrement des statistiques dans la table hero_stats
            for stat, value in self._stat.__dict__.items():
                cursor.execute('''
                    INSERT INTO hero_stats (hero_id, stat_name, stat_value)
                    VALUES (?, ?, ?)
                    ON CONFLICT(hero_id, stat_name) DO UPDATE SET
                        stat_value = excluded.stat_value
                ''', (Hero.id, stat, value))

            # Enregistrement des équipements dans la table hero_equipments
            cursor.execute('DELETE FROM hero_equipments WHERE hero_id = ?',
                           (Hero.id,))  # Supprime les anciens équipements
            for eq in self._equipment:
                cursor.execute('''
                    INSERT INTO hero_equipments (hero_id, equipment_name)
                    VALUES (?, ?)
                ''', (Hero.id, eq._name))

            # Enregistrement des objets du sac dans la table hero_bag
            cursor.execute('DELETE FROM hero_bag WHERE hero_id = ?', (Hero.id,))  # Supprime les anciens items
            for item in self.getBag():
                cursor.execute('''
                    INSERT INTO hero_bag (hero_id, item_name)
                    VALUES (?, ?)
                ''', (Hero.id, item._name))

            conn.commit()
            print(f"Héros {self._nom} sauvegardé avec succès dans la base de données.")
        except sqlite3.Error as e:
            print(f"Erreur lors de la sauvegarde en base de données : {e}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def load_by_id(hero_id):
        # Exemple avec SQL
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM heroes WHERE id = ?', (hero_id,))
        row = cursor.fetchone()
        if not row:
            return None

        targs = {
            'name': row['name'],
            'race': row['race'],
            'classe': row['classe'],
            'bag': [],  # Charge le sac si nécessaire
            'equipment': [],  # Charge l'équipement si nécessaire
            'element': row['element'],
            'profession': row['profession']
        }
        hero = Hero(targs)
        hero._xp = row['xp']
        hero._lvl = row['level']
        return hero

