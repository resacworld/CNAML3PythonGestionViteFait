from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import RG

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return '''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <title>Gestion Projet & Tâches - Création & Modification</title>
  <style>
    *, *::before, *::after {
      box-sizing: border-box;
    }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f7f9fc;
      color: #2c3e50;
      margin: 0;
      padding: 30px 20px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    h1 {
      color: #34495e;
      margin-bottom: 40px;
      font-weight: 700;
      text-align: center;
    }
    section {
      background: white;
      padding: 25px 30px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.12);
      margin-bottom: 40px;
      width: 100%;
      max-width: 700px;
    }
    h2 {
      margin-top: 0;
      margin-bottom: 20px;
      font-weight: 600;
      color: #34495e;
      border-bottom: 2px solid #2980b9;
      padding-bottom: 6px;
    }
    form {
      display: flex;
      flex-direction: column;
    }
    label {
      margin-bottom: 6px;
      font-weight: 600;
      font-size: 0.9rem;
      color: #34495e;
    }
    input[type="text"],
    input[type="email"],
    input[type="date"],
    select,
    textarea {
      padding: 10px 12px;
      margin-bottom: 20px;
      border: 1.5px solid #bdc3c7;
      border-radius: 5px;
      font-size: 1rem;
      transition: border-color 0.25s ease;
      resize: vertical;
      width: 100%;
      min-width: 150px;
    }
    input[type="text"]:focus,
    input[type="email"]:focus,
    input[type="date"]:focus,
    select:focus,
    textarea:focus {
      border-color: #2980b9;
      outline: none;
      background: #ecf6fd;
    }
    textarea {
      min-height: 80px;
    }
    button {
      align-self: flex-start;
      padding: 10px 24px;
      font-size: 1rem;
      background-color: #2980b9;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-weight: 700;
      transition: background-color 0.3s ease;
    }
    button:hover {
      background-color: #3498db;
    }
    /* Nouveau style flex-row wrap pour modifications */
    .inline-form {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
      gap: 20px 30px;
      align-items: flex-start;
    }
    .inline-form label {
      flex: 0 0 100%;
      margin-bottom: 6px;
    }
    .inline-form .form-group {
      display: flex;
      flex-direction: column;
      flex: 1 1 220px; /* largeur minimum = 220px, puis s'étire */
      min-width: 180px;
    }
    .inline-form button {
      flex: 0 0 auto;
      min-width: 140px;
      align-self: flex-end;
      margin-top: 24px;
    }
  </style>
</head>
<body>

<h1>Gestion Projets & Tâches - Création & Modification</h1>

<!-- Création Projet -->
<section aria-label="Création de Projet">
  <h2>Créer un Projet</h2>
  <form method="POST" action="/projects/create" autocomplete="off">
    <label for="project_title">Titre</label>
    <input type="text" id="project_title" name="title" required placeholder="Nom du projet">

    <label for="project_description">Description</label>
    <textarea id="project_description" name="description" placeholder="Description du projet"></textarea>

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

<!-- Modification Projet -->
<section aria-label="Modification de Projet">
  <h2>Modifier un Projet</h2>
  <form method="POST" action="/projects/update" autocomplete="off" class="inline-form">
    <div class="form-group">
      <label for="project_id_edit">ID Projet</label>
      <input type="text" id="project_id_edit" name="number" placeholder="ID du projet" required>
    </div>
    <div class="form-group">
      <label for="project_title_edit">Titre</label>
      <input type="text" id="project_title_edit" name="title" placeholder="Nouveau titre">
    </div>
    <div class="form-group">
      <label for="project_description_edit">Description</label>
      <textarea id="project_description_edit" name="description" placeholder="Nouvelle description" rows="3"></textarea>
    </div>
    <div class="form-group">
      <label for="project_begin_edit">Date début</label>
      <input type="date" id="project_begin_edit" name="begin">
    </div>
    <div class="form-group">
      <label for="project_end_edit">Date fin</label>
      <input type="date" id="project_end_edit" name="end">
    </div>
    <div class="form-group">
      <label for="project_advance_edit">Avancement (%)</label>
      <input type="text" id="project_advance_edit" name="advance" placeholder="Ex: 50">
    </div>
    <div class="form-group">
      <label for="project_status_edit">Statut</label>
      <input type="text" id="project_status_edit" name="status" placeholder="Nouveau statut">
    </div>
    <div class="form-group">
      <label for="project_priority_edit">Priorité</label>
      <input type="text" id="project_priority_edit" name="priority" placeholder="Nouvelle priorité">
    </div>
    <button type="submit">Modifier Projet</button>
  </form>
  <small>Entrez l'ID du projet à modifier, et renseignez uniquement les champs à changer.</small>
</section>

<!-- Création Tâche -->
<section aria-label="Création de Tâche">
  <h2>Créer une Tâche</h2>
  <form method="POST" action="/tasks/create" autocomplete="off">
    <label for="task_project">ID Projet</label>
    <input type="text" id="task_project" name="project" required placeholder="ID du projet">

    <label for="task_title">Titre</label>
    <input type="text" id="task_title" name="title" required placeholder="Nom de la tâche">

    <label for="task_description">Description</label>
    <textarea id="task_description" name="description" placeholder="Description de la tâche"></textarea>

    <label for="task_due_date">Date limite</label>
    <input type="date" id="task_due_date" name="due_date">

    <label for="task_status">Statut</label>
    <input type="text" id="task_status" name="status" placeholder="Ex: À faire">

    <label for="task_estimated">Date estimée</label>
    <input type="date" id="task_estimated" name="estimated">

    <label for="task_done">Date de fin</label>
    <input type="date" id="task_done" name="done">

    <label for="task_emergency">Urgence</label>
    <input type="text" id="task_emergency" name="emergency" placeholder="Ex: Moyenne">

    <button type="submit">Créer Tâche</button>
  </form>
</section>

<!-- Modification Tâche -->
<section aria-label="Modification de Tâche">
  <h2>Modifier une Tâche</h2>
  <form method="POST" action="/tasks/update" autocomplete="off" class="inline-form">
    <div class="form-group">
      <label for="task_id_edit">ID Tâche</label>
      <input type="text" id="task_id_edit" name="number" placeholder="ID de la tâche" required>
    </div>
    <div class="form-group">
      <label for="task_title_edit">Titre</label>
      <input type="text" id="task_title_edit" name="title" placeholder="Nouveau titre">
    </div>
    <div class="form-group">
      <label for="task_description_edit">Description</label>
      <textarea id="task_description_edit" name="description" placeholder="Nouvelle description" rows="2"></textarea>
    </div>
    <div class="form-group">
      <label for="task_due_date_edit">Date limite</label>
      <input type="date" id="task_due_date_edit" name="due_date">
    </div>
    <div class="form-group">
      <label for="task_status_edit">Statut</label>
      <input type="text" id="task_status_edit" name="status" placeholder="Nouveau statut">
    </div>
    <div class="form-group">
      <label for="task_estimated_edit">Date estimée</label>
      <input type="date" id="task_estimated_edit" name="estimated">
    </div>
    <div class="form-group">
      <label for="task_done_edit">Date de fin</label>
      <input type="date" id="task_done_edit" name="done">
    </div>
    <div class="form-group">
      <label for="task_emergency_edit">Urgence</label>
      <input type="text" id="task_emergency_edit" name="emergency" placeholder="Nouvelle urgence">
    </div>
    <button type="submit">Modifier Tâche</button>
  </form>
  <small>Indiquez l’ID de la tâche, puis modifiez les champs souhaités.</small>
</section>

<!-- Formulaires créés précédemment inchangés -->

<!-- Création Utilisateur -->
<section aria-label="Création Utilisateur">
  <h2>Créer un Utilisateur</h2>
  <form method="POST" action="/users/create" autocomplete="off">
    <label for="user_name">Nom</label>
    <input type="text" id="user_name" name="name" required placeholder="Nom">

    <label for="user_surname">Prénom</label>
    <input type="text" id="user_surname" name="surname" required placeholder="Prénom">

    <label for="user_mail">Email</label>
    <input type="email" id="user_mail" name="mail" required placeholder="email@example.com">

    <button type="submit">Créer Utilisateur</button>
  </form>
</section>

<!-- Création Rôle -->
<section aria-label="Création Rôle">
  <h2>Créer un Rôle</h2>
  <form method="POST" action="/roles/create" autocomplete="off">
    <label for="role_description">Description</label>
    <input type="text" id="role_description" name="description" required placeholder="Ex: Administrateur">

    <button type="submit">Créer Rôle</button>
  </form>
</section>

<!-- Création Grant -->
<section aria-label="Création Grant">
  <h2>Définir un Grant (Rôle d'un utilisateur sur un projet)</h2>
  <form method="POST" action="/grants/create" autocomplete="off">
    <label for="grant_project">ID Projet</label>
    <input type="text" id="grant_project" name="project" required>

    <label for="grant_user">ID Utilisateur</label>
    <input type="text" id="grant_user" name="user" required>

    <label for="grant_role">ID Rôle</label>
    <input type="text" id="grant_role" name="role" required>

    <button type="submit">Créer Grant</button>
  </form>
</section>

<!-- Création Allocation -->
<section aria-label="Allocation tâche-utilisateur">
  <h2>Allouer une tâche à un utilisateur</h2>
  <form method="POST" action="/alloc/create" autocomplete="off">
    <label for="alloc_task">ID Tâche</label>
    <input type="text" id="alloc_task" name="task" required>

    <label for="alloc_user">ID Utilisateur</label>
    <input type="text" id="alloc_user" name="user" required>

    <button type="submit">Allouer Tâche</button>
  </form>
</section>

<!-- Création Dépendance -->
<section aria-label="Création Dépendance entre tâches">
  <h2>Définir une dépendance entre tâches</h2>
  <form method="POST" action="/depend/create" autocomplete="off">
    <label for="depend_task_from">ID Tâche source</label>
    <input type="text" id="depend_task_from" name="task_from" required>

    <label for="depend_task_to">ID Tâche dépendante</label>
    <input type="text" id="depend_task_to" name="task_to" required>

    <button type="submit">Créer Dépendance</button>
  </form>
</section>

</body>
</html>

'''

# LISTING
@app.get("/projects")
def projects():
    return RG.mesProjects()

@app.get("/tasks")
def tasks():
    return RG.mesTasks()

@app.get("/users")
def users():
    return RG.mesUsers()

@app.get("/roles")
def roles():
    return RG.mesRoles()

@app.get("/grants")
def grants():
    return RG.mesGrants()

@app.get("/alloc")
def alloc():
    return RG.mesAlloc()

@app.get("/depend")
def depend():
    return RG.mesDepend()


# CREATE ROUTES
@app.post("/projects/create")
async def create_project(request: Request):
    data = dict(await request.form())
    RG.saveProject(data)
    return RedirectResponse("/", status_code=302)


@app.post("/tasks/create")
async def create_task(request: Request):
    data = dict(await request.form())
    RG.saveTask(data)
    return RedirectResponse("/", status_code=302)


@app.post("/users/create")
async def create_user(request: Request):
    data = dict(await request.form())
    RG.saveUser(data)
    return RedirectResponse("/", status_code=302)


@app.post("/roles/create")
async def create_role(request: Request):
    data = dict(await request.form())
    RG.saveRole(data)
    return RedirectResponse("/", status_code=302)


@app.post("/grants/create")
async def create_grant(request: Request):
    data = dict(await request.form())
    RG.saveGrant(data)
    return RedirectResponse("/", status_code=302)


@app.post("/alloc/create")
async def create_alloc(request: Request):
    data = dict(await request.form())
    RG.saveAlloc(data)
    return RedirectResponse("/", status_code=302)


@app.post("/depend/create")
async def create_depend(request: Request):
    data = dict(await request.form())
    RG.saveDepend(data)
    return RedirectResponse("/", status_code=302)


# UPDATE GENERIQUE
@app.get("/update")
def update(request: Request):
    params = dict(request.query_params)
    return RG.updateGeneric(params)


# SEARCH GENERIQUE
@app.get("/search/{query}")
def search(query: str):
    return RG.searchGeneric(query)
