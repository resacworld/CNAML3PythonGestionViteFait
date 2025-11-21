from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from RG import *

app = FastAPI()

@app.get("/")
def root():
    return '''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <title>Gestion Projet & Tâches - Formulaires</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { color: #2c3e50; }
    h2 { color: #34495e; margin-top: 40px; }
    form { margin-bottom: 30px; padding: 15px; border: 1px solid #ccc; border-radius: 5px; max-width: 600px;}
    label { display: block; margin: 8px 0 4px; }
    input[type="text"], input[type="email"], input[type="date"], select, textarea {
      width: 100%; padding: 8px; box-sizing: border-box; border: 1px solid #aaa; border-radius: 4px;
    }
    button { margin-top: 12px; padding: 10px 15px; background-color: #2980b9; color: white; border: none; border-radius: 4px; cursor: pointer;}
    button:hover { background-color: #3498db; }
  </style>
</head>
<body>

<h1>Gestion Projets et Tâches - Création d'entités</h1>

<!-- Formulaire Projet -->
<section>
  <h2>Créer un Projet</h2>
  <form method="POST" action="/projects/create">
    <label for="project_title">Titre</label>
    <input type="text" id="project_title" name="title" required>

    <label for="project_description">Description</label>
    <textarea id="project_description" name="description"></textarea>

    <label for="project_begin">Date début</label>
    <input type="date" id="project_begin" name="begin">

    <label for="project_end">Date fin</label>
    <input type="date" id="project_end" name="end">

    <label for="project_advance">Avancement (%)</label>
    <input type="text" id="project_advance" name="advance" placeholder="Ex: 50">

    <label for="project_status">Statut</label>
    <input type="text" id="project_status" name="status" placeholder="Ex: En cours">

    <label for="project_priority">Priorité</label>
    <input type="text" id="project_priority" name="priority" placeholder="Ex: Haute">

    <button type="submit">Créer Projet</button>
  </form>
</section>

<!-- Formulaire Tâche -->
<section>
  <h2>Créer une Tâche</h2>
  <form method="POST" action="/tasks/create">
    <label for="task_project">ID Projet</label>
    <input type="text" id="task_project" name="project" required>

    <label for="task_title">Titre</label>
    <input type="text" id="task_title" name="title" required>

    <label for="task_description">Description</label>
    <textarea id="task_description" name="description"></textarea>

    <label for="task_due_date">Date limite</label>
    <input type="date" id="task_due_date" name="due_date">

    <label for="task_status">Statut</label>
    <input type="text" id="task_status" name="status" placeholder="Ex: À faire">

    <label for="task_estimated">Estimation (date)</label>
    <input type="date" id="task_estimated" name="estimated">

    <label for="task_done">Terminé (date)</label>
    <input type="date" id="task_done" name="done">

    <label for="task_emergency">Urgence</label>
    <input type="text" id="task_emergency" name="emergency" placeholder="Ex: Moyenne">

    <button type="submit">Créer Tâche</button>
  </form>
</section>

<!-- Formulaire Utilisateur -->
<section>
  <h2>Créer un Utilisateur</h2>
  <form method="POST" action="/users/create">
    <label for="user_name">Nom</label>
    <input type="text" id="user_name" name="name" required>

    <label for="user_surname">Prénom</label>
    <input type="text" id="user_surname" name="surname" required>

    <label for="user_mail">Email</label>
    <input type="email" id="user_mail" name="mail" required>

    <button type="submit">Créer Utilisateur</button>
  </form>
</section>

<!-- Formulaire Rôle -->
<section>
  <h2>Créer un Rôle</h2>
  <form method="POST" action="/roles/create">
    <label for="role_description">Description</label>
    <input type="text" id="role_description" name="description" required>

    <button type="submit">Créer Rôle</button>
  </form>
</section>

<!-- Formulaire GRANTS (Rôles utilisateurs sur projets) -->
<section>
  <h2>Définir un Grant (Rôle d'un utilisateur sur un projet)</h2>
  <form method="POST" action="/grants/create">
    <label for="grant_project">ID Projet</label>
    <input type="text" id="grant_project" name="project" required>

    <label for="grant_user">ID Utilisateur</label>
    <input type="text" id="grant_user" name="user" required>

    <label for="grant_role">ID Rôle</label>
    <input type="text" id="grant_role" name="role" required>

    <button type="submit">Créer Grant</button>
  </form>
</section>

<!-- Formulaire ALLOC (Allocation de tâche) -->
<section>
  <h2>Allouer une tâche à un utilisateur</h2>
  <form method="POST" action="/alloc/create">
    <label for="alloc_task">ID Tâche</label>
    <input type="text" id="alloc_task" name="task" required>

    <label for="alloc_user">ID Utilisateur</label>
    <input type="text" id="alloc_user" name="user" required>

    <button type="submit">Allouer Tâche</button>
  </form>
</section>

<!-- Formulaire DEPEND (Dépendance entre tâches) -->
<section>
  <h2>Définir une dépendance entre tâches</h2>
  <form method="POST" action="/depend/create">
    <label for="depend_task_from">ID Tâche source (dont dépend)</label>
    <input type="text" id="depend_task_from" name="task_from" required>

    <label for="depend_task_to">ID Tâche cible (dépendante)</label>
    <input type="text" id="depend_task_to" name="task_to" required>

    <button type="submit">Créer Dépendance</button>
  </form>
</section>

</body>
</html>
'''

# @app.get("/test", response_class=HTMLResponse)
# def test():
#     return "<html><head><title>Test Page</title></head><body><h1>This is a test page</h1></body></html>"

@app.get("/projects")
def projects():
    return mesProjects()
