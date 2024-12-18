CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_login TEXT NOT NULL,
        user_password TEXT NOT NULL,
        user_mail TEXT UNIQUE NOT NULL,
        user_date_new DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_date_login DATETIME,
        user_compte_id INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS equipements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT, 
    type_objet TEXT, 
    rarete TEXT, 
    effet TEXT,
    equipe BOOLEAN,
    proprietaire INTEGER,
    FOREIGN KEY(proprietaire) REFERENCES heros(id)
);

CREATE TABLE IF NOT EXISTS consommables (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT, 
    type_objet TEXT, 
    rarete TEXT, 
    effet TEXT, 
    quantite INTEGER,
    proprietaire INTEGER,
    FOREIGN KEY(proprietaire) REFERENCES heros(id)
);

CREATE TABLE IF NOT EXISTS heros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    race TEXT NOT NULL,
    classe TEXT NOT NULL,
    niveau INTEGER DEFAULT 1,
    experience INTEGER DEFAULT 0,
    proprietaire INTEGER,
    -- Stats de base d'Avatar
    force INTEGER DEFAULT 5,
    endurance INTEGER DEFAULT 5,
    agilite INTEGER DEFAULT 5,
    -- Bonus d'équipement
    force_bonus INTEGER DEFAULT 0,
    endurance_bonus INTEGER DEFAULT 0,
    agilite_bonus INTEGER DEFAULT 0,
    -- Points de vie
    points_vie INTEGER,
    points_vie_max INTEGER,
    -- Position
    position INTEGER DEFAULT 0,
    FOREIGN KEY(proprietaire) REFERENCES user(id)
);