from ..RPG_PLATEAU.rpg_objet import Equipement, Raretes
from flask import session
import sqlite3
from typing import Optional

class EquipementDb(Equipement):
    """Classe gérant la persistance des équipements en base de données"""

    def __init__(self, equipement: Equipement, proprietaire: int = None):
        self.__dict__.update(equipement.__dict__)
        self.proprietaire = proprietaire

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('game.db')
        conn.row_factory = sqlite3.Row
        return conn

    def save(self):
        """Sauvegarde ou met à jour l'équipement en base"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        if getattr(self, "id", None) is None:
            cursor.execute('''
                INSERT INTO equipements (
                    nom, type_objet, rarete, effet, equipe, proprietaire
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.nom, self.type_objet, self.rarete.value, str(self.effet), 
                self.equipe, self.proprietaire
            ))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE equipements SET
                    nom = ?, type_objet = ?, rarete = ?, effet = ?, 
                    equipe = ?, proprietaire = ?
                WHERE id = ?
            ''', (
                self.nom, self.type_objet, self.rarete.value, str(self.effet), 
                self.equipe, self.proprietaire, self.id
            ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(id: int) -> Optional['EquipementDb']:
        """Récupère un équipement depuis la base par son ID"""
        conn = EquipementDb.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM equipements WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            equipement = Equipement(
                nom=row['nom'],
                type_objet=row['type_objet'],
                rarete=Raretes(row['rarete']),
                effet=eval(row['effet']),
                equipe=row['equipe']
            )
            equipement.id = row['id']
            equipement.proprietaire = row['proprietaire']
            return EquipementDb(equipement, row['proprietaire'])
        return None
