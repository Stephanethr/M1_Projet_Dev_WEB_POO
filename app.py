import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session
from back.RPG_DATABASE.heros_db import HerosDb
from back.RPG_DATABASE.equipement_db import EquipementDb
from back.RPG_DATABASE.consommable_db import ConsommableDb
from back.RPG_PLATEAU.rpg_objet import Equipement, Consommable
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from init_db import get_db_connection
from back.RPG_PLATEAU.rpg_heros import *
from back.RPG_PLATEAU.rpg_avatar import *
from back.RPG_DATABASE.heros_db import *

# Charger les variables d'environnement
load_dotenv()

# Initialiser l'application Flask
app = Flask(__name__)

# Charger la clé secrète depuis le fichier .env pour sécuriser les sessions
app.secret_key = os.getenv('SECRET_KEY')

# Initialiser Bcrypt pour le hachage des mots de passe
bcrypt = Bcrypt(app)

# Route pour la page d'accueil (affiche des informations sur l'utilisateur connecté)
@app.route('/')
def home():
    if 'loggedin' not in session:
        flash("Veuillez vous connecter.", 'info')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les informations de l'utilisateur
    cursor.execute('SELECT user_login, user_date_new, user_date_login FROM user WHERE user_id = ?', (session['user_id'],))
    user = cursor.fetchone()

    if not user:
        session.clear()
        flash("Votre session est invalide. Veuillez vous reconnecter.", 'danger')
        return redirect(url_for('login'))

    # Récupérer les héros associés à l'utilisateur
    cursor.execute('SELECT * FROM heros WHERE proprietaire = ?', (session['user_id'],))
    heroes = cursor.fetchall()

    # Mettre les héros en session
    session['heroes'] = [dict(hero) for hero in heroes]

    conn.close()

    return render_template(
        'home.html',
        loggedin=True,
        user_name=user['user_login'],
        user_last_login=user['user_date_login'],
        heroes=session['heroes']
    )

@app.route('/view_hero/<int:hero_id>')
def view_hero(hero_id):
    if 'loggedin' not in session:
        flash("Veuillez vous connecter.", 'info')
        return redirect(url_for('login'))

    hero = HerosDb.get_by_id(hero_id)
    if not hero or hero.proprietaire != session['user_id']:
        flash("Héros introuvable ou accès non autorisé.", 'danger')
        return redirect(url_for('home'))
    
    # Charger les équipements et consommables du héros
    conn = EquipementDb.get_db_connection()
    cursor = conn.cursor()

    # Récupération des équipements
    cursor.execute('SELECT * FROM equipements WHERE proprietaire = ?', (hero_id,))
    equipments = [EquipementDb.get_by_id(row['id']) for row in cursor.fetchall()]

    # Récupération des consommables
    cursor.execute('SELECT * FROM consommables WHERE proprietaire = ?', (hero_id,))
    consumables = [ConsommableDb.get_by_id(row['id']) for row in cursor.fetchall()]

    conn.close()

    hero.inventaire = []
    hero.agilite_bonus = 0
    hero.endurance_bonus = 0
    hero.force_bonus = 0

    for e in equipments:
        temp_obj = Equipement(e.nom, e.type_objet, e.rarete, e.effet, e.equipe)
        hero.ajouter_objet_inventaire(temp_obj)
    
    hero._recalculer_pv()

    # Stockage en session
    session['equipments'] = [equip.id for equip in equipments]
    session['consumables'] = [cons.id for cons in consumables]

    # Formattage des données

    return render_template('view_hero.html', hero=hero,
    equipments=equipments,
    consumables=consumables)

@app.route('/hero/<int:hero_id>/toggle_equipment/<int:equip_id>')
def toggle_equipment(hero_id, equip_id):

    # Charger l'équipement
    equip = EquipementDb.get_by_id(equip_id)
    print(equip)
    if not equip or equip.proprietaire != hero_id:
        flash("Équipement introuvable ou non autorisé.", 'warning')
        return redirect(url_for('view_hero', hero_id=hero_id))

    # Inversion de l'état "équipé"
    equip.equipe = not equip.equipe
    equip.save()  # Mise à jour en base

    # Notification à l'utilisateur
    action = "équipé" if equip.equipe else "déséquipé"
    flash(f"L'équipement {equip.nom} a été {action} avec succès.", 'success')

    # Retour à la vue du héros
    return redirect(url_for('view_hero', hero_id=hero_id))

@app.route('/insert_hero', methods=['POST'])
def insert_hero():
    if 'loggedin' not in session:
        flash("Veuillez vous connecter.", 'info')
        return redirect(url_for('login'))

    # Récupérer les données du formulaire
    name = request.form.get('name')
    classe = request.form.get('classe')
    race = request.form.get('race')

    # Vérifications des champs obligatoires
    if not name or not classe or not race:
        flash("Tous les champs sont obligatoires pour créer un héros.", 'danger')
        return redirect(url_for('create_hero_form'))

    try:
        # Convertir les valeurs en enums
        class_type = ClassType(classe)
        race_type = RaceType(race)
    except ValueError:
        flash("Classe ou race invalide.", 'danger')
        return redirect(url_for('create_hero'))

    try:
        # Créer le héros
        hero = Heros(name, race_type, class_type)

        # Sauvegarder le héros dans la base de données
        hero_db = HerosDb(hero)
        hero_db.proprietaire = session['user_id']
        hero_db.save()

        flash(f"Héros {name} créé avec succès !", 'success')
    except ValueError as e:
        # Gestion des erreurs de validation dans la classe `Heros`
        flash(str(e), 'danger')
        return redirect(url_for('create_hero_form'))

    return redirect(url_for('home'))

@app.route('/create_hero', methods=['GET'])
def create_hero():
    if 'loggedin' not in session:
        flash("Veuillez vous connecter.", 'info')
        return redirect(url_for('login'))

    return render_template('create_hero.html')


@app.route('/heroes')
def list_heroes():
    if 'loggedin' not in session:
        flash("Veuillez vous connecter.", 'info')
        return redirect(url_for('login'))

    # Récupérer les héros de l'utilisateur connecté (par exemple via une requête SQL ou un fichier)
    user_id = session['user_id']
    # Supposons que tu as une méthode statique `Hero.load_by_user_id` pour récupérer tous les héros d'un utilisateur
    heroes = Hero.load_by_user_id(user_id)

    return render_template('heroes.html', heroes=heroes)

@app.route('/edit_hero/<int:hero_id>', methods=['GET', 'POST'])
def edit_hero(hero_id):
    if 'loggedin' not in session:
        flash("Veuillez vous connecter.", 'info')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les informations du héros
    cursor.execute('SELECT * FROM heroes WHERE id = ? AND user_id = ?', (hero_id, session['user_id']))
    hero = cursor.fetchone()

    if not hero:
        flash("Héros introuvable ou non autorisé.", 'danger')
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form['name']
        classe = request.form['classe']

        if not name or not classe:
            flash("Tous les champs sont obligatoires.", 'danger')
            return redirect(url_for('edit_hero', hero_id=hero_id))

        # Mettre à jour le héros dans la base de données
        cursor.execute('UPDATE heroes SET name = ?, classe = ? WHERE id = ?', (name, classe, hero_id))
        conn.commit()
        flash("Héros mis à jour avec succès.", 'success')
        return redirect(url_for('home'))

    cursor.close()
    conn.close()

    return render_template('edit_hero.html', hero=hero)

@app.route('/update_hero/<int:hero_id>', methods=['POST'])
def update_hero(hero_id):
    if 'loggedin' not in session:
        flash("Veuillez vous connecter.", 'info')
        return redirect(url_for('login'))

    xp_gained = int(request.form.get('xp', 0))
    if xp_gained <= 0:
        flash("XP invalide.", 'danger')
        return redirect(url_for('list_heroes'))

    # Charger le héros (par exemple via une méthode statique Hero.load_by_id)
    hero = Hero.load_by_id(hero_id)

    if not hero:
        flash("Héros introuvable.", 'danger')
        return redirect(url_for('list_heroes'))

    # Ajouter l'expérience et mettre à jour
    hero.setXP(xp_gained)
    hero.save()

    flash(f"Le héros {hero._nom} a gagné {xp_gained} XP et est maintenant niveau {hero._lvl} !", 'success')
    return redirect(url_for('list_heroes'))


# Route pour se connecter
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Vérifier les champs obligatoires
        if not email or not password:
            flash('Tous les champs sont obligatoires !', 'danger')
            return redirect(url_for('login'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE user_mail = ?', (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Vérifier si l'utilisateur existe et si le mot de passe est correct
        if user and bcrypt.check_password_hash(user['user_password'], password):
            session['loggedin'] = True
            session['user_id'] = user['user_id']
            session['username'] = user['user_login']
            flash('Connexion réussie!', 'success')
            # Rediriger directement vers l'inventaire après connexion
            return redirect(url_for('home'))
        else:
            flash('Email ou mot de passe incorrect !', 'danger')

    return render_template('login.html')

# Route pour s'inscrire
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        recheck_password = request.form['recheck_password']

        # Vérifier les champs obligatoires
        if not email or not username or not password or not recheck_password:
            flash('Tous les champs sont obligatoires !', 'danger')
            return redirect(url_for('register'))

        # Vérifier si les mots de passe correspondent
        if password != recheck_password:
            flash('Les mots de passe ne correspondent pas !', 'danger')
            return redirect(url_for('register'))

        # Hacher le mot de passe
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()
        # Vérifier si l'email est déjà utilisé
        cursor.execute('SELECT * FROM user WHERE user_mail = ?', (email,))
        account = cursor.fetchone()

        if account:
            flash('Cet email est déjà utilisé!', 'danger')
        else:
            # Insérer le nouvel utilisateur dans la base de données
            cursor.execute(
                'INSERT INTO user (user_login, user_password, user_mail) VALUES (?, ?, ?)',
                (username, hashed_password, email)
            )
            conn.commit()
            session['loggedin'] = True
            session['user_id'] = cursor.lastrowid
            session['username'] = username
            flash('Compte créé avec succès !', 'success')
            return redirect(url_for('home'))

        cursor.close()
        conn.close()

    return render_template('register.html')

# Route pour se déconnecter
@app.route('/logout', methods=['POST'])
def logout():
    # Supprimer toutes les données de session pour déconnecter l'utilisateur
    session.clear()
    flash('Vous avez été déconnecté !', 'success')
    return redirect(url_for('login'))


# Route pour afficher l'inventaire de l'utilisateur connecté
@app.route('/inventory')
def inventory():
    # Vérifier si l'utilisateur est connecté
    if 'loggedin' not in session:
        flash('Veuillez vous connecter pour accéder à votre inventaire.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les informations de l'utilisateur connecté
    cursor.execute('SELECT user_login FROM user WHERE user_id = ?', (session['user_id'],))
    user = cursor.fetchone()
    username = user['user_login'] if user else 'Utilisateur'

    # Récupérer les items de l'inventaire de l'utilisateur connecté
    cursor.execute('''
        SELECT inventory.id AS item_id, inventory.name AS item_name, 
               item_types.type_name AS item_type, inventory.quantity AS item_quantity 
        FROM inventory 
        JOIN item_types ON inventory.type_id = item_types.id 
        WHERE inventory.user_id = ?
    ''', (session['user_id'],))
    items = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('inventory.html', items=items, username=username)

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if 'loggedin' not in session:
        flash('Veuillez vous connecter pour ajouter un item.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les types d'objets pour le sélecteur
    cursor.execute('SELECT * FROM item_types')
    item_types = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        type_id = request.form['type_id']
        quantity = request.form['quantity']

        if not name or not type_id or not quantity:
            flash('Tous les champs sont obligatoires !', 'danger')
            return redirect(url_for('add_item'))

        # Insérer le nouvel item dans la base de données
        cursor.execute('INSERT INTO inventory (user_id, name, type_id, quantity) VALUES (?, ?, ?, ?)',
                       (session['user_id'], name, type_id, quantity))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Objet ajouté avec succès !', 'success')
        return redirect(url_for('inventory'))

    cursor.close()
    conn.close()
    return render_template('edit_item.html', action='Ajouter', item=None, item_types=item_types)


@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    if 'loggedin' not in session:
        flash('Veuillez vous connecter.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Supprimer l'objet avec l'ID donné
    cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
    conn.commit()
    cursor.close()
    conn.close()

    flash('Objet supprimé avec succès !', 'success')
    return redirect(url_for('inventory'))


@app.route('/consume/<int:item_id>', methods=['POST'])
def consume_item(item_id):
    if 'loggedin' not in session:
        flash('Veuillez vous connecter.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer l'item pour vérifier s'il existe
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (item_id,))
    item = cursor.fetchone()

    # Vérifier si l'item existe et si la quantité est suffisante
    if item and item['quantity'] > 0:
        new_quantity = item['quantity'] - 1
        cursor.execute('UPDATE inventory SET quantity = ? WHERE id = ?', (new_quantity, item_id))
        conn.commit()
        flash('Objet consommé avec succès !', 'success')
    else:
        flash('Quantité insuffisante ou objet non trouvé.', 'danger')

    cursor.close()
    conn.close()
    return redirect(url_for('inventory'))

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    if 'loggedin' not in session:
        flash('Veuillez vous connecter pour modifier un item.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Récupérer les informations de l'item à modifier
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (item_id,))
    item = cursor.fetchone()

    if not item:
        flash("L'objet n'existe pas.", 'danger')
        return redirect(url_for('inventory'))

    # Récupérer les types d'objets pour le sélecteur
    cursor.execute('SELECT * FROM item_types')
    item_types = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        type_id = request.form['type_id']
        quantity = request.form['quantity']

        if not name or not type_id or not quantity:
            flash('Tous les champs sont obligatoires !', 'danger')
            return redirect(url_for('edit_item', item_id=item_id))

        # Mettre à jour l'item dans la base de données
        cursor.execute('UPDATE inventory SET name = ?, type_id = ?, quantity = ? WHERE id = ?',
                       (name, type_id, quantity, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Objet modifié avec succès !', 'success')
        return redirect(url_for('inventory'))

    cursor.close()
    conn.close()
    return render_template('edit_item.html', action='Modifier', item=item, item_types=item_types)

# Lancer l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
