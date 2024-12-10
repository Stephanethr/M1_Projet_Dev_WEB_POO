import sqlite3
import os

# Chemin vers la base de données SQLite
DATABASE_PATH = os.getenv('DATABASE_PATH', 'game.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Créer la table `user`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_login TEXT NOT NULL,
        user_password TEXT NOT NULL,
        user_mail TEXT UNIQUE NOT NULL,
        user_date_new DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_date_login DATETIME,
        user_compte_id INTEGER DEFAULT 0
    )
    ''')

    # Créer la table `item_types`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS item_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type_name TEXT NOT NULL
    )
    ''')

    # Ajouter des types d'objets par défaut
    cursor.execute('''
    INSERT OR IGNORE INTO item_types (id, type_name) 
    VALUES 
        (1, 'potion'), 
        (2, 'plante'), 
        (3, 'arme'), 
        (4, 'clé'), 
        (5, 'armure')
    ''')

    # Créer la table `inventory` associée à chaque utilisateur
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT NOT NULL,
        type_id INTEGER,
        quantity INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES user(user_id),
        FOREIGN KEY (type_id) REFERENCES item_types(id)
    )
    ''')

    # Créer la table `heroes`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        race TEXT NOT NULL,
        classe TEXT NOT NULL,
        level INTEGER NOT NULL DEFAULT 1,
        xp INTEGER NOT NULL DEFAULT 0,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user(user_id)
    )
    ''')

    # Créer la table `hero_stats`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hero_stats (
        hero_id INTEGER NOT NULL,
        stat_name TEXT NOT NULL,
        stat_value INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY (hero_id, stat_name),
        FOREIGN KEY (hero_id) REFERENCES heroes(id)
    )
    ''')

    # Créer la table `hero_equipments`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hero_equipments (
        hero_id INTEGER NOT NULL,
        equipment_name TEXT NOT NULL,
        PRIMARY KEY (hero_id, equipment_name),
        FOREIGN KEY (hero_id) REFERENCES heroes(id)
    )
    ''')

    # Créer la table `hero_bag`
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hero_bag (
        hero_id INTEGER NOT NULL,
        item_name TEXT NOT NULL,
        PRIMARY KEY (hero_id, item_name),
        FOREIGN KEY (hero_id) REFERENCES heroes(id)
    )
    ''')

    # Ajouter d'autres tables ou relations si nécessaire...

    conn.commit()
    cursor.close()
    conn.close()
    print("Base de données initialisée avec succès.")

if __name__ == '__main__':
    init_db()
