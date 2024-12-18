from ..RPG_PLATEAU.rpg_objet import Consommable, Raretes
from flask import session
import sqlite3
from typing import Optional

class ConsommableDb(Consommable):
    """Classe gérant la persistance des consommables en base de données"""

    def __init__(self, consommable: Consommable, proprietaire: int = None):
        self.__dict__.update(consommable.__dict__)
        self.proprietaire = proprietaire

    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('game.db')
        conn.row_factory = sqlite3.Row
        return conn

    def save(self):
        """Sauvegarde ou met à jour le consommable en base"""
        conn = self.get_db_connection()
        cursor = conn.cursor()

        if getattr(self, "id", None) is None:
            cursor.execute('''
                INSERT INTO consommables (
                    nom, type_objet, rarete, effet, quantite, proprietaire
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.nom, self.type_objet, self.rarete.value, str(self.effet), 
                self.quantite, self.proprietaire
            ))
            self.id = cursor.lastrowid
        else:
            cursor.execute('''
                UPDATE consommables SET
                    nom = ?, type_objet = ?, rarete = ?, effet = ?, 
                    quantite = ?, proprietaire = ?
                WHERE id = ?
            ''', (
                self.nom, self.type_objet, self.rarete.value, str(self.effet), 
                self.quantite, self.proprietaire, self.id
            ))

        conn.commit()
        conn.close()

    @staticmethod
    def get_by_id(id: int) -> Optional['ConsommableDb']:
        """Récupère un consommable depuis la base par son ID"""
        conn = ConsommableDb.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM consommables WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            consommable = Consommable(
                nom=row['nom'],
                type_objet=row['type_objet'],
                rarete=Raretes(row['rarete']),
                effet=eval(row['effet']),
                quantite=row['quantite']
            )
            consommable.id = row['id']
            consommable.proprietaire = row['proprietaire']
            return consommable
        return None
