import sqlite3
import re
from db import fetch_all, insert, update, search_all, init_db

init_db()


# ======== LISTING ========

def mesProjects():
    return fetch_all("PROJECTS")

def mesTasks():
    return fetch_all("TASKS")
   
def mesUsers():
    return fetch_all("USERS")

def mesRoles():
    return fetch_all("ROLES")

def mesGrants():
    return fetch_all("GRANTS")

def mesAlloc():
    return fetch_all("ALLOC")

def mesDepend():
    return fetch_all("DEPEND")

# ======== SAVE (CREATE) ========

def verifier_user(data):
    
    name, surname, mail = data.get("name"), data.get("surname"), data.get("mail")
    
# 1. Nettoyage et vérification si les champs sont vides
    name = name.strip() if name else ""
    surname = surname.strip() if surname else ""
    mail = mail.strip() if mail else ""

    if not name or not surname or not mail:
        return False

    # 2. Vérification simplifiée du format email
    # Structure : texte + @ + texte + . + texte
    if not re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        return False

    # Si on arrive ici, tout est valide
    return True

def verifier_projet(data):
    
    title, description, begin, end, advance, status, priority = data.get("title"), data.get("description"), data.get("begin"), data.get("end"), data.get("advance"), data.get("status"), data.get("priority")

    # 1. Nettoyage des textes
    title = title.strip() if title else ""
    description = description.strip() if description else ""
    
    # 2. Vérification des champs obligatoires
    if not title or not description:
        return False

    # 3. Vérification du format des dates (AAAA-MM-JJ)
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(date_pattern, str(begin)) or not re.match(date_pattern, str(end)):
        return False

    # 4. Vérification de la progression (0 à 100)
    if not (0 <= int(advance) <= 100):
        return False

    # 5. Vérification de la priorité (1 à 5)
    if not (1 <= int(priority) <= 5):
        return False

    # 6. Vérification du statut (liste autorisée)
    statuts_valides = ["À faire", "En cours", "Terminé", "En pause"]
    if status not in statuts_valides:
        return False

    return True

def verifier_task(data):

    project, title, description, due_date, status, estimated, done, emergency = data.get("project"), data.get("title"), data.get("description"), data.get("due_date"), data.get("status"), data.get("estimated"), data.get("done"), data.get("emergency")

    # 1. Nettoyage et vérification des champs obligatoires
    title = title.strip() if title else ""
    description = description.strip() if description else ""
    
    if not title or not description or project is None:
        return False

    # 2. Vérification du format de la date (AAAA-MM-JJ)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(due_date)):
        return False

    # 3. Vérification des nombres (doivent être positifs)
    try:
        if int(estimated) < 0 or int(done) < 0:
            return False
    except (ValueError, TypeError):
        return False

    # 4. Vérification de l'urgence (1 à 5)
    if not (1 <= int(emergency) <= 5):
        return False

    # 5. Vérification du statut
    if status not in ["À faire", "En cours", "Terminé"]:
        return False

    return True

def verifier_grant(data):

    project_id, user_id, role_id = data.get("project_id"), data.get("user_id"), data.get("role_id")

    # 1. Vérification que les IDs ne sont pas vides (None)
    if project_id is None or user_id is None or role_id is None:
        return False

    # 2. Vérification que ce sont bien des nombres entiers
    # (indispensable pour les clés étrangères)
    try:
        project_id = int(project_id)
        user_id = int(user_id)
        role_id = int(role_id)
    except (ValueError, TypeError):
        return False

    # 3. Règle : Les IDs doivent être strictement supérieurs à 0
    # (Un ID auto-incrémenté en SQL commence à 1)
    if project_id <= 0 or user_id <= 0 or role_id <= 0:
        return False

    return True

def verifier_alloc(data):

    task_id, user_id = data.get("task_id"), data.get("user_id")

    # 1. Vérification que les IDs ne sont pas vides
    if task_id is None or user_id is None:
        return False

    # 2. Vérification du type (doit être convertible en entier)
    try:
        task_id = int(task_id)
        user_id = int(user_id)
    except (ValueError, TypeError):
        return False

    # 3. Règle : Les identifiants SQL commencent à 1
    if task_id <= 0 or user_id <= 0:
        return False

    return True

def verifier_depend(data):

    task_from_id, task_to_id = data.get("task_from_id"), data.get("task_to_id")

    # 1. Vérification que les IDs ne sont pas vides
    if task_from_id is None or task_to_id is None:
        return False

    # 2. Vérification du type (nombres entiers)
    try:
        t_from = int(task_from_id)
        t_to = int(task_to_id)
    except (ValueError, TypeError):
        return False

    # 3. Règle : Les IDs doivent être positifs
    if t_from <= 0 or t_to <= 0:
        return False

    # 4. Règle de gestion métier : Une tâche ne peut pas dépendre d'elle-même
    # (Cela créerait une boucle infinie)
    if t_from == t_to:
        return False

    return True

def saveProject(data):
    
    #insert("PROJECTS", data)
    return verifier_projet(data)

def saveTask(data):
    #insert("TASKS", data)
    return verifier_task(data)

def saveUser(data):
    #insert("USERS", data)
    return verifier_user(data)

def saveRole(data):
    #insert("ROLES", data)
    return {"status": "Rôle enregistré"}

def saveGrant(data):
    #insert("GRANTS", data)
    return verifier_grant(data)

def saveAlloc(data):
    #insert("ALLOC", data)
    return verifier_alloc(data)

def saveDepend(data):
    #insert("DEPEND", data)
    return verifier_depend(data)


# ======== UPDATE GENERIQUE ========

def updateGeneric(params):
    mapping = {
        "project": "PROJECTS",
        "task": "TASKS",
        "user": "USERS",
        "role": "ROLES",
        "grant": "GRANTS",
        "alloc": "ALLOC",
        "depend": "DEPEND",
    }

    for key in mapping:
        if key in params:
            table = mapping[key]
            record_id = params.pop(key, None)
            if record_id and record_id.isdigit():
                update(table, int(record_id), params)
                return { "status": f"{table} modifié" }
            else:
                #insert(table, params)
                return { "status": f"{table} créé" }

    return {"error": "Aucune table reconnue"}


# ======== SEARCH GENERIQUE ========

def searchGeneric(query):
    if query.upper() in ["PROJECT", "PROJECTS"]:
        return fetch_all("PROJECTS")
    if query.upper() in ["TASK", "TASKS"]:
        return fetch_all("TASKS")
    if query.upper() in ["USER", "USERS"]:
        return fetch_all("USERS")
    if query.upper() in ["ROLE", "ROLES"]:
        return fetch_all("ROLES")
    if query.upper() in ["GRANT", "GRANTS"]:
        return fetch_all("GRANTS")
    if query.upper() in ["ALLOC"]:
        return fetch_all("ALLOC")
    if query.upper() in ["DEPEND"]:
        return fetch_all("DEPEND")

    return search_all(query)

def render_projects_rows():
    projects = fetch_all("PROJECTS")
    rows = []

    for p in projects:
        number   = p[0]
        title    = p[1]
        desc     = p[2]
        begin    = p[3]
        end      = p[4]
        advance  = p[5]
        status   = p[6]
        priority = p[7]

        rows.append(f"""
    <tr>
      <td style="font-weight:600;">{number}</td>

      <td>
        <strong>{title}</strong><br>
        <small style="color:#6b7280;">{desc}</small>
      </td>

      <td>
        <span class="badge status-{status.lower().replace(' ', '-')}">
          {status}
        </span>
      </td>

      <td>
        <div class="progress">
          <div class="progress-bar" style="width:{advance}%;">
            {advance}%
          </div>
        </div>
      </td>

      <td>
        <span class="badge priority-{priority.lower().replace(' ', '-')}">
          {priority}
        </span>
      </td>

      <td>{end}</td>

      <td style="text-align:center;">
        <!-- ✏️ MODIFIER -->
        <a href="/projects/edit/{number}"
          title="Modifier"
          style="color:#2563eb; margin-right:12px;">
          <i class="fas fa-pen"></i>
        </a>

        <!-- 🗑️ SUPPRIMER -->
        <form method="POST"
              action="/projects/delete/{number}"
              style="display:inline;"
              onsubmit="return confirm('Supprimer ce projet ?');">
          <button type="submit"
                  style="background:none; border:none; color:#ef4444; cursor:pointer;">
            <i class="fas fa-trash"></i>
          </button>
        </form>
      </td>
    </tr>
  """)


    return "\n".join(rows), len(projects)



def page_html():
    with open("templates/dashboard.html", "r", encoding="utf-8") as f:
        html = f.read()

    project_rows, count = render_projects_rows()

    html = html.replace("{{PROJECT_ROWS}}", project_rows)
    html = html.replace("{{PROJECT_COUNT}}", str(count))

    return html
    
def page_html_old():
    return'''
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Tableau de Bord - Gestion Projets & Tâches</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"/>
  <style>
    :root {
      --primary: #2563eb; --primary-dark: #1d4ed8; --success: #10b981;
      --warning: #f59e0b; --danger: #ef4444; --gray-100: #f3f4f6;
      --gray-200: #e5e7eb; --gray-600: #4b5563; --gray-800: #1f2937;
      --shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 4px 6px -2px rgba(0,0,0,0.05);
      --radius: 12px;
    }
    * { margin:0; padding:0; box-sizing:border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #f0f2f5 0%, #e0e7ff 100%);
      color: var(--gray-800);
      min-height: 100vh;
      padding-top: 80px;
    }
    header {
      position: fixed; top:0; left:0; right:0; background:white;
      padding:1rem 2rem; box-shadow:0 4px 20px rgba(0,0,0,0.08); z-index:1000;
      display:flex; align-items:center; justify-content:space-between;
    }
    header h1 { font-size:1.6rem; color:var(--primary); font-weight:700; }
    .container { max-width:1450px; margin:0 auto; padding:2rem; }
    .dashboard-grid {
      display:grid;
      grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
      gap:1.8rem;
      margin-top:2rem;
    }
    .card {
      background:white; border-radius:var(--radius);
      box-shadow:var(--shadow); overflow:hidden;
      transition:transform .3s, box-shadow .3s;
    }
    .card:hover { transform:translateY(-8px); box-shadow:0 20px 35px -10px rgba(0,0,0,0.15); }
    .card-header {
      background:var(--primary); color:white; padding:1rem 1.5rem;
      font-weight:600; font-size:1.1rem; display:flex; align-items:center; gap:0.7rem;
    }
    .card-body { padding:1.5rem; }
    .tabs { display:flex; background:var(--gray-100); border-radius:8px; overflow:hidden; margin-bottom:1.5rem; }
    .tab { flex:1; padding:0.8rem; text-align:center; background:transparent; border:none; font-weight:600; cursor:pointer; transition:.3s; }
    .tab.active { background:var(--primary); color:white; }
    .tab-content { display:none; }
    .tab-content.active { display:block; }
    form { display:grid; gap:1rem; }
    .form-row { display:grid; grid-template-columns:1fr 1fr; gap:1rem; }
    @media (max-width:640px) { .form-row { grid-template-columns:1fr; } }
    label { font-weight:600; color:var(--gray-800); font-size:0.95rem; margin-bottom:0.4rem; display:block; }
    input, textarea, select {
      width:100%; padding:0.75rem 1rem; border:2px solid var(--gray-200);
      border-radius:8px; font-size:1rem; transition:.2s;
    }
    input:focus, textarea:focus, select:focus {
      outline:none; border-color:var(--primary); box-shadow:0 0 0 3px rgba(37,99,235,0.15);
    }
    button {
      background:var(--primary); color:white; border:none; padding:0.8rem 1.6rem;
      border-radius:8px; font-weight:600; cursor:pointer; transition:.3s;
      display:inline-flex; align-items:center; gap:0.5rem;
    }
    button:hover { background:var(--primary-dark); transform:translateY(-2px); }
    small { color:var(--gray-600); font-size:0.85rem; margin-top:1rem; display:block; }

    /* Table styles */
    table { width:100%; border-collapse:collapse; font-size:0.95rem; }
    th { background:var(--gray-100); text-align:left; padding:1rem; cursor:pointer; user-select:none; }
    th i { opacity:0.4; margin-left:4px; }
    td { padding:1rem; border-bottom:1px solid var(--gray-200); }
    tr:hover { background:#f8faff; }
    .badge {
      padding:0.35rem 0.75rem; border-radius:50px; font-size:0.8rem; font-weight:600;
    }
    .status-en-cours   { background:#dbeafe; color:#1e40af; }
    .status-termine    { background:#d1fae5; color:#065f46; }
    .status-bloque     { background:#fee2e2; color:#991b1b; }
    .status-en-attente { background:#fef3c7; color:#92400e; }
    .priority-critique { background:#fee2e2; color:#991b1b; }
    .priority-haute    { background:#fecaca; color:#7f1d1d; }
    .priority-moyenne  { background:#fef3c7; color:#92400e; }
    .priority-basse    { background:#f3f4f6; color:#4b5563; }
    .progress {
      height:8px; background:var(--gray-200); border-radius:4px; overflow:hidden; margin:8px 0;
    }
    .progress-bar {
      height:100%; background:var(--primary); border-radius:4px;
      transition:width .4s; font-size:0.75rem; color:white; text-align:right;
      padding-right:6px; line-height:8px;
    }
    .progress-bar.success { background:var(--success); }
    .progress-bar.warning { background:var(--warning); }
  </style>
</head>
<body>

<header>
  <div>
    <h1>Gestion Projets & Tâches</h1>
    <div style="font-size:0.9rem; color:var(--gray-600);">Tableau de bord administrateur</div>
  </div>
  <div style="font-size:1.8rem; color:var(--primary);">Dashboard</div>
</header>

<div class="container">
  <div class="dashboard-grid">

    <!-- 1. Gestion Projets -->
    <div class="card">
      <div class="card-header">Gestion des Projets</div>
      <div class="card-body">
        <div class="tabs">
          <button class="tab active" onclick="openTab(event,'create-project')">Créer</button>
          <button class="tab" onclick="openTab(event,'edit-project')">Modifier</button>
        </div>
        <div id="create-project" class="tab-content active">
          <form method="POST" action="/projects/create">
            <div class="form-row">
              <div><label>Titre</label><input type="text" name="title" required></div>
              <div><label>Date début</label><input type="date" name="begin"></div>
            </div>
            <label>Description</label><textarea name="description" rows="3"></textarea>
            <div class="form-row">
              <div><label>Date fin</label><input type="date" name="end"></div>
              <div><label>Avancement (%)</label><input type="text" name="advance" placeholder="50"></div>
            </div>
            <div class="form-row">
              <div><label>Statut</label><input type="text" name="status" placeholder="En cours"></div>
              <div><label>Priorité</label><input type="text" name="priority" placeholder="Haute"></div>
            </div>
            <button type="submit">Créer le projet</button>
          </form>
        </div>
        <div id="edit-project" class="tab-content">
          <form method="POST" action="/projects/update">
            <label>ID Projet</label><input type="text" name="number" required placeholder="123">
            <div class="form-row">
              <div><label>Nouveau titre</label><input type="text" name="title"></div>
              <div><label>Avancement</label><input type="text" name="advance"></div>
            </div>
            <button type="submit">Mettre à jour</button>
          </form>
          <small>Ne remplir que les champs à modifier</small>
        </div>
      </div>
    </div>

    <!-- 2. Gestion Tâches -->
    <div class="card">
      <div class="card-header">Gestion des Tâches</div>
      <div class="card-body">
        <div class="tabs">
          <button class="tab active" onclick="openTab(event,'create-task')">Créer</button>
          <button class="tab" onclick="openTab(event,'edit-task')">Modifier</button>
        </div>
        <div id="create-task" class="tab-content active">
          <form method="POST" action="/tasks/create">
            <div class="form-row">
              <div><label>ID Projet</label><input type="text" name="project" required></div>
              <div><label>Titre</label><input type="text" name="title" required></div>
            </div>
            <label>Description</label><textarea name="description" rows="2"></textarea>
            <div class="form-row">
              <div><label>Date limite</label><input type="date" name="due_date"></div>
              <div><label>Statut</label><input type="text" name="status" placeholder="À faire"></div>
            </div>
            <button type="submit">Créer la tâche</button>
          </form>
        </div>
        <div id="edit-task" class="tab-content">
          <form method="POST" action="/tasks/update">
            <label>ID Tâche</label><input type="text" name="number" required>
            <div class="form-row">
              <div><label>Nouveau statut</label><input type="text" name="status"></div>
              <div><label>Date de fin</label><input type="date" name="done"></div>
            </div>
            <button type="submit">Mettre à jour</button>
          </form>
        </div>
      </div>
    </div>

    <!-- 3. Utilisateurs & Rôles -->
    <div class="card">
      <div class="card-header">Utilisateurs & Rôles</div>
      <div class="card-body">
        <form method="POST" action="/users/create" style="margin-bottom:1.5rem;">
          <div class="form-row">
            <div><label>Nom</label><input type="text" name="name" required></div>
            <div><label>Prénom</label><input type="text" name="surname" required></div>
          </div>
          <label>Email</label><input type="email" name="mail" required>
          <button type="submit">Créer utilisateur</button>
        </form>
        <form method="POST" action="/roles/create">
          <label>Nouveau rôle</label><input type="text" name="description" placeholder="ex: Chef de projet" required>
          <button type="submit">Créer rôle</button>
        </form>
      </div>
    </div>

    <!-- 4. Permissions & Allocations -->
    <div class="card">
      <div class="card-header">Permissions & Allocations</div>
      <div class="card-body">
        <form method="POST" action="/grants/create" style="margin-bottom:1rem;">
          <div class="form-row">
            <div><label>ID Projet</label><input type="text" name="project" required></div>
            <div><label>ID User</label><input type="text" name="user" required></div>
            <div><label>ID Rôle</label><input type="text" name="role" required></div>
          </div>
          <button type="submit">Accorder rôle</button>
        </form>
        <form method="POST" action="/alloc/create">
          <div class="form-row">
            <div><label>ID Tâche</label><input type="text" name="task" required></div>
            <div><label>ID Utilisateur</label><input type="text" name="user" required></div>
          </div>
          <button type="submit">Allouer tâche</button>
        </form>
      </div>
    </div>

    <!-- 5. Dépendances -->
    <div class="card">
      <div class="card-header">Dépendances entre tâches</div>
      <div class="card-body">
        <form method="POST" action="/depend/create">
          <div class="form-row">
            <div><label>Tâche source</label><input type="text" name="task_from" required placeholder="ID tâche A"></div>
            <div><label>Tâche dépendante</label><input type="text" name="task_to" required placeholder="ID tâche B"></div>
          </div>
          <button type="submit">Créer dépendance</button>
        </form>
      </div>
    </div>

    <!-- 6. LISTE COMPLÈTE DES PROJETS -->
    <div class="card" style="grid-column:1/-1;">
      <div class="card-header">
        Liste complète des projets
        <span style="margin-left:auto; opacity:0.9;">
          <i class="fas fa-sync-alt" style="cursor:pointer;" title="Actualiser" onclick="loadProjects()"></i>
        </span>
      </div>
      <div class="card-body" style="padding:0;">
        <div style="overflow-x:auto;">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Projet</th>
                <th>Statut</th>
                <th style="width:150px;">Avancement</th>
                <th>Priorité</th>
                <th>Date fin</th>
              </tr>
            </thead>
            <tbody id="projectsList">
              <!-- Projets chargés dynamiquement ici -->
              <!-- Exemples statiques (sera remplacé par le JS) -->
              <tr>
                <td style="font-weight:600;">101</td>
                <td><strong>Refonte site corporate</strong><br><small style="color:#6b7280;">Migration Next.js + API</small></td>
                <td><span class="badge status-en-cours">En cours</span></td>
                <td>
                  <div class="progress"><div class="progress-bar" style="width:68%;">68%</div></div>
                </td>
                <td><span class="badge priority-haute">Haute</span></td>
                <td>28/02/2026</td>
              </tr>
              <tr>
                <td style="font-weight:600;">98</td>
                <td><strong>Application mobile</strong><br><small style="color:#6b7280;">iOS & Android</small></td>
                <td><span class="badge status-termine">Terminé</span></td>
                <td>
                  <div class="progress"><div class="progress-bar success" style="width:100%;">100%</div></div>
                </td>
                <td><span class="badge priority-moyenne">Moyenne</span></td>
                <td>15/11/2025</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div style="padding:1rem; text-align:center; color:#6b7280; font-size:0.9rem; border-top:1px solid var(--gray-200);">
          <span id="projectCount">2</span> projet(s) • Dernière mise à jour : <span id="lastUpdate">à l'instant</span>
        </div>
      </div>
    </div>

  </div>
</div>
</body>
</html>


'''