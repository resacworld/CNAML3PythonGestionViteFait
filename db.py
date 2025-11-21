import sqlite3
from sqlite3 import Connection

def tables():
    try:
        conn = sqlite3.connect('database.db')
    except sqlite3.Error as e:
        print(e)
        return False
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS PROJECTS (titre TEXT, description TEXT)''')
    return True

def ajouterProjects():
    try:
        conn = sqlite3.connect('database.db')
    except sqlite3.Error as e:
        print(e)
        return False
    c = conn.cursor()
    c.execute("INSERT INTO PROJECTS (titre, description) VALUES ('Projet1', 'Description1'), ('Projet2', 'Description2'), ('Projet3', 'Description3')")
    conn.commit()
    conn.close()
    return True


def listeTable(nomTable: str):
    try:
        conn = sqlite3.connect('database.db')
    except sqlite3.Error as e:
        print(e)
        return False
    c = conn.cursor()
    c.execute(f"SELECT * FROM {nomTable}")
    rows = c.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    print(tables())
    print(ajouterProjects())
    print(listeTable("PROJECTS"))