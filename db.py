import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db(): # Initialisation de la base de données et création des tables si elles n'existent pas 
    conn = get_connection()
    c = conn.cursor()

    # ===== Création des tables =====

    # Table PROJECTS
    c.execute("""
    CREATE TABLE IF NOT EXISTS PROJECTS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        begin TEXT,
        end TEXT,
        advance INTEGER,
        status TEXT,
        priority TEXT
    )
    """)

    # Table TASKS
    c.execute("""
    CREATE TABLE IF NOT EXISTS TASKS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project INTEGER,
        title TEXT,
        description TEXT,
        due_date TEXT,
        status TEXT,
        estimated TEXT,
        done TEXT,
        emergency TEXT
    )
    """)

    # Table USERS
    c.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        mail TEXT
    )
    """)

    # Table ROLES
    c.execute("""
    CREATE TABLE IF NOT EXISTS ROLES (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT
    )
    """)

    # Table GRANTS
    c.execute("""
    CREATE TABLE IF NOT EXISTS GRANTS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project INTEGER,
        user INTEGER,
        role INTEGER
    )
    """)

    # Table ALLOC
    c.execute("""
    CREATE TABLE IF NOT EXISTS ALLOC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task INTEGER,
        user INTEGER
    )
    """)

    # Table DEPEND
    c.execute("""
    CREATE TABLE IF NOT EXISTS DEPEND (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_from INTEGER,
        task_to INTEGER
    )
    """)

    conn.commit()
    conn.close()


def fetch_all(table): # Récupère toutes les entrées d'une table donnée
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table}")
    rows = c.fetchall()
    conn.close()
    return rows

def fetch_tasks_for_project(project_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT id, title, status, due_date
        FROM TASKS
        WHERE project = ?
    """, (project_id,))
    rows = c.fetchall()
    conn.close()
    return rows



def insert(table, data: dict): # Insère une nouvelle entrée dans une table donnée
    conn = get_connection()
    c = conn.cursor()

    keys = ", ".join(data.keys())
    values = tuple(data.values())
    placeholders = ", ".join(["?"] * len(data))

    query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
    c.execute(query, values)

    conn.commit()
    conn.close()


def update(table, record_id, data: dict): # Met à jour une entrée existante dans une table donnée
    conn = get_connection()
    c = conn.cursor()

    fields = ", ".join([f"{k}=?" for k in data.keys()])
    values = list(data.values())
    values.append(record_id)

    query = f"UPDATE {table} SET {fields} WHERE id=?"
    c.execute(query, values)

    conn.commit()
    conn.close()


def search_all(keyword): # Recherche générique dans toutes les tables et colonnes
    conn = get_connection()
    c = conn.cursor()

    results = {}
    tables = ["PROJECTS", "TASKS", "USERS", "ROLES", "GRANTS", "ALLOC", "DEPEND"]

    for table in tables:
        c.execute(f"PRAGMA table_info({table})")
        cols = [col[1] for col in c.fetchall()]

        query = " OR ".join([f"{col} LIKE ?" for col in cols])
        values = [f"%{keyword}%"] * len(cols)

        c.execute(f"SELECT * FROM {table} WHERE {query}", values)
        results[table] = c.fetchall()

    conn.close()
    return results


def delete_project_db(project_id): # Supprime un projet de la base de données
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM PROJECTS WHERE id=?", (project_id,))
    conn.commit()
    conn.close()


def getProjectById(project_id): # Récupère un projet par son ID
    """
    Retourne un projet sous forme de dictionnaire :
    {
      "title": "...",
      "description": "...",
      "begin": "...",
      "end": "...",
      "advance": 50,
      "status": "...",
      "priority": "..."
    }
    """
    try:
        project_id = int(project_id)
    except (ValueError, TypeError):
        return None

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT title, description, begin, end, advance, status, priority
        FROM PROJECTS
        WHERE id = ?
    """, (project_id,))

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    project_dict = {
        "title": row[0],
        "description": row[1],
        "begin": row[2],
        "end": row[3],
        "advance": row[4],
        "status": row[5],
        "priority": row[6]
    }

    return project_dict

def delete_task_db(task_id): # Supprime une tâche de la base de données
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM TASKS WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def delete_user_db(user_id): # Supprime un utilisateur de la base de données
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM USERS WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def delete_role_db(role_id): # Supprime un rôle de la base de données
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM ROLES WHERE id=?", (role_id,))
    conn.commit()
    conn.close()

def delete_grant_db(grant_id): # Supprime un droit de la base de données
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM GRANTS WHERE id=?", (grant_id,))
    conn.commit()
    conn.close()

def delete_alloc_db(alloc_id): # Supprime une alloc de la base de données
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM ALLOC WHERE id=?", (alloc_id,))
    conn.commit()
    conn.close()
