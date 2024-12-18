from ..RPG_PLATEAU.rpg_heros import Heros, RaceType, ClassType
from flask import session
import sqlite3
from typing import Optional
import random

class HerosDb(Heros):
    """Classe gérant la persistance des héros en base de données"""
    
    def __init__(self, heros: Heros):
        # On copie tous les attributs du héros
        self.id = None
        self.__dict__.update(heros.__dict__)
        
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('game.db')
        conn.row_factory = sqlite3.Row
        return conn

    def save(self):
        """Sauvegarde ou met à jour le héros en base"""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        print(self.__dict__)

        if self.id is None:
            self.id = random.randint(1, 1000000)
            cursor.execute('''
                INSERT INTO heros (
                    nom, race, classe, niveau, experience, proprietaire,
                    force, endurance, agilite,
                    force_bonus, endurance_bonus, agilite_bonus,
                    points_vie, points_vie_max, position
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.name, self.race.value, self.classe.value,
                self.niveau, self.experience, self.proprietaire,
                self.force, self.endurance, self.agilite,
                self.force_bonus, self.endurance_bonus, self.agilite_bonus,
                self.points_vie, self.points_vie_max, self.position
            ))
            self.id = cursor.lastrowid
            # Mise à jour de l'ID en session si c'est le héros courant
            if session.get('current_hero_id') is None:
                session['current_hero_id'] = self.id
        else:
            cursor.execute('''
                UPDATE heros SET
                    nom = ?, race = ?, classe = ?, niveau = ?, experience = ?, 
                    proprietaire = ?, force = ?, endurance = ?, agilite = ?,
                    force_bonus = ?, endurance_bonus = ?, agilite_bonus = ?,
                    points_vie = ?, points_vie_max = ?, position = ?
                WHERE id = ?
            ''', (
                self.name, self.race.value, self.classe.value,
                self.niveau, self.experience, self.proprietaire,
                self.force, self.endurance, self.agilite,
                self.force_bonus, self.endurance_bonus, self.agilite_bonus,
                self.points_vie, self.points_vie_max, self.position,
                self.id
            ))
        
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(id: int) -> Optional['HerosDb']:
        """Récupère un héros depuis la base par son ID"""
        conn = HerosDb.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM heros WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            # On crée d'abord un héros de base
            heros = Heros(
                name=row['nom'],
                race_type=RaceType(row['race']),
                class_type=ClassType(row['classe'])
            )
            # Puis on met à jour ses attributs avec les données de la DB
            heros.id = row['id']
            heros.experience = row['experience']
            heros.niveau = row['niveau']
            heros.proprietaire = row['proprietaire']
            heros.force = row['force']
            heros.endurance = row['endurance']
            heros.agilite = row['agilite']
            heros.force_bonus = row['force_bonus']
            heros.endurance_bonus = row['endurance_bonus']
            heros.agilite_bonus = row['agilite_bonus']
            heros.points_vie = row['points_vie']
            heros.points_vie_max = row['points_vie_max']
            heros.position = row['position']
            
            # On retourne une instance de HerosDb
            return HerosDb(heros)
        return None

    @staticmethod
    def get_current_hero() -> Optional['HerosDb']:
        """Récupère le héros courant depuis la session Flask"""
        hero_id = session.get('current_hero_id')
        if hero_id is not None:
            return HerosDb.get_by_id(hero_id)
        return None

    @staticmethod
    def set_current_hero(hero_id: int):
        """Définit le héros courant dans la session Flask"""
        session['current_hero_id'] = hero_id

    def __getattribute__(self, name):
        """Surcharge pour sauvegarder automatiquement après certaines méthodes"""
        attr = super().__getattribute__(name)
        
        # Liste des méthodes qui modifient l'état et nécessitent une sauvegarde
        methods_to_save = [
            'niveau_suivant',
            'gagner_experience',
            'deplacer',
            'penaliser',
            'equiper_objet',
            'desequiper_objet',
            'ajouter_objet_inventaire',
            'retirer_objet_inventaire',
            'consommer_objet',
            'recevoir_degats'
        ]
        
        if callable(attr) and name in methods_to_save:
            def wrapper(*args, **kwargs):
                result = attr(*args, **kwargs)
                self.save()  # Sauvegarde automatique après l'exécution
                return result
            return wrapper
            
        return attr