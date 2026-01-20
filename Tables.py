import sqlite3 # Gestion de la base de données SQLite

def create_tables(): # Fonction pour créer les tables dans la base de données SQLite
    try:
        conn = sqlite3.connect('database.db') # connexion à la base de données Sqlite (database.db)
    except sqlite3.Error as e:
        print(e)
        return False

    c = conn.cursor() # Créer un curseur pour executer les commandes SQL

    # TABLE PROJECTS
    c.execute('''
        CREATE TABLE IF NOT EXISTS PROJECTS (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            begin TEXT,
            end TEXT,
            advance INTEGER,
            status TEXT,
            priority INTEGER
        )
    ''')

    # TABLE USERS
    c.execute('''
        CREATE TABLE IF NOT EXISTS USERS (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            mail TEXT
        )
    ''')

    # TABLE ROLES
    c.execute('''
        CREATE TABLE IF NOT EXISTS ROLES (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT
        )
    ''')

    # TABLE TASKS
    c.execute('''
        CREATE TABLE IF NOT EXISTS TASKS (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            project INTEGER,
            title TEXT,
            description TEXT,
            due_date TEXT,
            status TEXT,
            estimated INTEGER,
            done INTEGER,
            emergency INTEGER,
            FOREIGN KEY(project) REFERENCES PROJECTS(number)
        )
    ''')

    # TABLE ALLOC
    c.execute('''
        CREATE TABLE IF NOT EXISTS ALLOC (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            task INTEGER,
            user INTEGER,
            FOREIGN KEY(task) REFERENCES TASKS(number),
            FOREIGN KEY(user) REFERENCES USERS(number)
        )
    ''')

    # TABLE DEPEND
    c.execute('''
        CREATE TABLE IF NOT EXISTS DEPEND (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            task_from INTEGER,
            task_to INTEGER,
            FOREIGN KEY(task_from) REFERENCES TASKS(number),
            FOREIGN KEY(task_to) REFERENCES TASKS(number)
        )
    ''')

    # TABLE GRANTS
    c.execute('''
        CREATE TABLE IF NOT EXISTS GRANTS (
            number INTEGER PRIMARY KEY AUTOINCREMENT,
            project INTEGER,
            user INTEGER,
            role INTEGER,
            FOREIGN KEY(project) REFERENCES PROJECTS(number),
            FOREIGN KEY(user) REFERENCES USERS(number),
            FOREIGN KEY(role) REFERENCES ROLES(number)
        )
    ''')

    conn.commit() # Enregistrer les modifications
    conn.close() # Fermer la connexion
    return True # Retourner True si la création des tables a réussi
