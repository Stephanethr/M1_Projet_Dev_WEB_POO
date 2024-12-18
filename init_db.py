import sqlite3
import os

def get_db_connection():
    # Assurez-vous que le dossier instance existe
    conn = sqlite3.connect('game.db')
    conn.row_factory = sqlite3.Row  # Pour avoir accès aux colonnes par leur nom
    return conn

def init_db():
    conn = get_db_connection()
    try:
        with open('schema.sql') as f:
            conn.executescript(f.read())
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
