import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    c = conn.cursor()

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

    c.execute("""
    CREATE TABLE IF NOT EXISTS USERS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        surname TEXT,
        mail TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ROLES (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS GRANTS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project INTEGER,
        user INTEGER,
        role INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS ALLOC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task INTEGER,
        user INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS DEPEND (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_from INTEGER,
        task_to INTEGER
    )
    """)

    conn.commit()
    conn.close()


def fetch_all(table):
    conn = get_connection()
    c = conn.cursor()
    c.execute(f"SELECT * FROM {table}")
    rows = c.fetchall()
    conn.close()
    return rows


def insert(table, data: dict):
    conn = get_connection()
    c = conn.cursor()

    keys = ", ".join(data.keys())
    values = tuple(data.values())
    placeholders = ", ".join(["?"] * len(data))

    query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
    c.execute(query, values)

    conn.commit()
    conn.close()


def update(table, record_id, data: dict):
    conn = get_connection()
    c = conn.cursor()

    fields = ", ".join([f"{k}=?" for k in data.keys()])
    values = list(data.values())
    values.append(record_id)

    query = f"UPDATE {table} SET {fields} WHERE id=?"
    c.execute(query, values)

    conn.commit()
    conn.close()


def search_all(keyword):
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


def delete_project_db(project_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM PROJECTS WHERE id=?", (project_id,))
    conn.commit()
    conn.close()

def delete_task_db(task_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM TASKS WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def delete_user_db(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM USERS WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def delete_role_db(role_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM ROLES WHERE id=?", (role_id,))
    conn.commit()
    conn.close()

def delete_grant_db(grant_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM GRANTS WHERE id=?", (grant_id,))
    conn.commit()
    conn.close()

def delete_alloc_db(alloc_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM ALLOC WHERE id=?", (alloc_id,))
    conn.commit()
    conn.close()