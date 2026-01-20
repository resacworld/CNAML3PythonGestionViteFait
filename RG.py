import sqlite3                                                      # Gestion de la base de données SQLite
import re                                                           # Module pour les expressions régulières    
from datetime import datetime                                       # Expressions regulières pour validation
from db import fetch_all, insert, update, search_all, init_db       # Fonction de gestion de la BDD Base de données 

init_db()


# ======== LISTING ========

def mesProjects():
    return fetch_all("PROJECTS") # Récupèere tous les projects de la table Projects

def mesTasks():
    return fetch_all("TASKS")    # Récupère tous les task de la table Tasks
   
def mesUsers():
    return fetch_all("USERS")    # Récupère tous les users de la table USERS

def mesRoles():
    return fetch_all("ROLES")   # Récupère tous les roles de la table ROLES

def mesGrants():
    return fetch_all("GRANTS")  # Récupère tous les grants de la table GRANTS

def mesAlloc():
    return fetch_all("ALLOC")   # Récupère tous les alloc de la table ALLOC

def mesDepend():
    return fetch_all("DEPEND")  # Récupère tous les depend de la table DEPEND

# ======== SAVE (CREATE) ========

def verifier_user(data):
    
    name, surname, mail = data.get("name"), data.get("surname"), data.get("mail") # Récupère les données du dictionnaire data
    
# Nettoyage et vérification si les champs sont vides
    name = name.strip() if name else ""
    surname = surname.strip() if surname else ""
    mail = mail.strip() if mail else ""

    if not name or not surname or not mail:
        return False

    # Vérification du format email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        return False

    # tout est valide
    return True

def verifier_projet(data):
    
    title, description, begin, end, advance, status, priority = data.get("title"), data.get("description"), data.get("begin"), data.get("end"), data.get("advance"), data.get("status"), data.get("priority") # Récupère les données du dictionnaire data
    #print(title, description, begin, end, advance, status, priority)

    # Nettoyage des textes
    title = title.strip() if title else ""
    description = description.strip() if description else ""
    
    # Vérification des champs obligatoires
    if not title or not description:
        return False

    # Vérification du format des dates (AAAA-MM-JJ)
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(date_pattern, str(begin)) or not re.match(date_pattern, str(end)):
        return False
    
    # 4. Vérification de si la date de début est antérieure à la date de fin
    if datetime.strptime(str(begin), "%Y-%m-%d") > datetime.strptime(str(end), "%Y-%m-%d"):
        return False

    # Vérification de la progression (0 à 100)
    if not (0 <= int(advance) <= 100):
        return False

    # 5. Vérification de la priorité (1 à 5)
    if not str(priority) in ["Critique", "Haute", "Moyenne", "Basse"]:
       return False

    # 6. Vérification du statut (liste autorisée)
    statuts_valides = ["A faire", "En cours", "Terminé", "En attente", "Bloqué"]
    if status not in statuts_valides:
       return False

    return True

def verifier_task(data):

    project, title, description, due_date, status, estimated, done, emergency = data.get("project"), data.get("title"), data.get("description"), data.get("due_date"), data.get("status"), data.get("estimated"), data.get("done"), data.get("emergency") # Récupère les données du dictionnaire data
    print(project, title, description, due_date, status, estimated, done, emergency)
    # Nettoyage et vérification des champs obligatoires
    title = title.strip() if title else ""
    description = description.strip() if description else ""
    
    if not title or not description or project is None:
        return False

    # Vérification du format de la date (AAAA-MM-JJ)
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(due_date)):
        return False

    # Vérification des nombres (doivent être positifs)
    # try:
    #     if int(estimated) < 0 or int(done) < 0:
    #         return False
    # except (ValueError, TypeError):
    #     return False

    # Vérification de l'urgence (1 à 5)
    #if not (1 <= int(emergency) <= 5):
    #    return False

    # Vérification du statut
    #if status not in ["À faire", "En cours", "Terminé"]:
    #    return False

    print("vrai task")
    return True

def verifier_grant(data):

    project_id, user_id, role_id = data.get("project_id"), data.get("user_id"), data.get("role_id") # Récupère les données du dictionnaire data

    # Vérification que les IDs ne sont pas vides (None)
    if project_id is None or user_id is None or role_id is None:
        return False

    # Vérification que ce sont bien des nombres entiers
    # (indispensable pour les clés étrangères)
    try:
        project_id = int(project_id)
        user_id = int(user_id)
        role_id = int(role_id)
    except (ValueError, TypeError):
        return False

    # Règle : Les IDs doivent être strictement supérieurs à 0
    # (Un ID auto-incrémenté en SQL commence à 1)
    if project_id <= 0 or user_id <= 0 or role_id <= 0:
        return False

    return True

def verifier_alloc(data):

    task_id, user_id = data.get("task_id"), data.get("user_id")

    # Vérification que les IDs ne sont pas vides
    if task_id is None or user_id is None:
        return False

    # Vérification du type (doit être convertible en entier)
    try:
        task_id = int(task_id)
        user_id = int(user_id)
    except (ValueError, TypeError):
        return False

    # Règle : Les identifiants SQL commencent à 1
    if task_id <= 0 or user_id <= 0:
        return False

    return True

def verifier_depend(data):

    task_from_id, task_to_id = data.get("task_from_id"), data.get("task_to_id")

    # Vérification que les IDs ne sont pas vides
    if task_from_id is None or task_to_id is None:
        return False

    # Vérification du type (nombres entiers)
    try:
        t_from = int(task_from_id)
        t_to = int(task_to_id)
    except (ValueError, TypeError):
        return False

    # Règle : Les IDs doivent être positifs
    if t_from <= 0 or t_to <= 0:
        return False

    # Règle de gestion métier : Une tâche ne peut pas dépendre d'elle-même
    if t_from == t_to:
        return False

    return True

def saveProject(data):
    
    #insert("PROJECTS", data)
    return verifier_projet(data) # Vérifie les données du projet avant de l'enregistrer

def saveTask(data):
    #insert("TASKS", data)
    return verifier_task(data) # Vérifie les données du task avant de l'enregistrer

def saveUser(data):
    #insert("USERS", data)
    return verifier_user(data) # Vérifie les données de l'utilisateur avant de l'enregistrer

def saveRole(data):
    #insert("ROLES", data)
    return {"status": "Rôle enregistré"} # Pas de vériification spécifique pour les rôles

def saveGrant(data):
    #insert("GRANTS", data)
    return verifier_grant(data) # Vérifie les données du grant avant de l'enregistrer

def saveAlloc(data):
    #insert("ALLOC", data)
    return verifier_alloc(data) # Vérifie les données de l'allocation avant de l'enregistrer
def saveDepend(data):
    #insert("DEPEND", data)
    return verifier_depend(data) # Vérifie les données de la dépendance avant de l'enregistrer
# ======== UPDATE GENERIQUE ========

def updateGeneric(params): # Met à jour une entrée générique dans la base de données  en fonction des paramètres données 
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

def searchGeneric(query): # Recherche générique dans la base de données en fonction de la requête données
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

def render_projects_rows(): # Génère les lignes HTML pour la liste des projets 
    projects = fetch_all("PROJECTS")
    rows = []

    for p in projects:
        number   = p[0] # identifiant
        title    = p[1] # titre
        desc     = p[2] # description
        begin    = p[3] # date début 
        end      = p[4] # date fin
        advance  = p[5] # 0 à 100
        status   = p[6] # en cours, termine, en attente, bloque, a faire
        priority = p[7] # Critique, haute, moyenne, basse

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
        <!-- MODIFIER -->
        <a href="/projects/edit/{number}"
          title="Modifier"
          style="color:#2563eb; margin-right:12px;">
          <i class="fas fa-pen"></i>
        </a>

        <!-- SUPPRIMER -->
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

def render_user_rows():
    users = fetch_all("USERS")

    rows = []
    for u in users:
        user_id = u[0]
        name    = u[1]
        surname = u[2]
        mail    = u[3]

        rows.append(f"""
        <tr>
        <td style="font-weight:600;">{user_id}</td>
        <td>{name} {surname}</td>
        <td>{mail}</td>
        <td style="text-align:center;">
            <form method="POST"
                action="/users/delete/{user_id}"
                style="display:inline;"
                onsubmit="return confirm('Supprimer cet utilisateur ?');">
            <button type="submit"
                    style="background:none; border:none; color:#ef4444; cursor:pointer;">
                <i class="fas fa-trash"></i>
            </button>
            </form>
        </td>
        </tr>
        """) 
    return "\n".join(rows)

def page_html(mode="main", project=None): # Génère la page HTML du tableau de bord 
    html = open("templates/dashboard.html").read()

    if mode == "edit" and project:
        # Remplacer les placeholders par les valeurs du projet
        html = html \
            .replace("{{FORM_ACTION}}", f"/projects/update/{project['id']}") \
            .replace("{{TITLE}}", project['title']) \
            .replace("{{DESCRIPTION}}", project['description']) \
            .replace("{{BEGIN}}", project['begin'] or "") \
            .replace("{{END}}", project['end'] or "") \
            .replace("{{ADVANCE}}", str(project['advance'])) \
            .replace("{{STATUS}}", project['status']) \
            .replace("{{PRIORITY}}", project['priority']) \
            .replace("{{PRIORITY_CRITIQUE}}", "selected" if project["priority"] == "Critique" else "") \
            .replace("{{PRIORITY_HAUTE}}", "selected" if project["priority"] == "Haute" else "") \
            .replace("{{PRIORITY_MOYENNE}}", "selected" if project["priority"] == "Moyenne" else "") \
            .replace("{{PRIORITY_BASSE}}", "selected" if project["priority"] == "Basse" else "") \
            .replace("{{STATUS_EN_COURS}}", "selected" if project["status"] == "En cours" else "") \
            .replace("{{STATUS_TERMINE}}", "selected" if project["status"] == "Terminé" else "") \
            .replace("{{STATUS_EN_ATTENTE}}", "selected" if project["status"] == "En attente" else "") \
            .replace("{{STATUS_BLOQUE}}", "selected" if project["status"] == "Bloqué" else "") \
            .replace("{{STATUS_A_FAIRE}}", "selected" if project["status"] == "A faire" else "")

    else:
        html = html \
          .replace("{{FORM_ACTION}}", "/projects/create") \
          .replace("{{TITLE}}", "") \
          .replace("{{DESCRIPTION}}", "") \
          .replace("{{BEGIN}}", "") \
          .replace("{{END}}", "") \
          .replace("{{ADVANCE}}", "") \
          .replace("{{STATUS}}", "") \
          .replace("{{PRIORITY}}", "") \
          .replace("{{PRIORITY_CRITIQUE}}", "") \
          .replace("{{PRIORITY_HAUTE}}", "") \
          .replace("{{PRIORITY_MOYENNE}}", "") \
          .replace("{{PRIORITY_BASSE}}", "") \
          .replace("{{ADVANCE}}", str(0)) 
          

    project_rows, count = render_projects_rows() # Génère les lignes HTML pour la liste des projets
    html = html.replace("{{PROJECT_ROWS}}", project_rows) # Insère les lignes dans le template HTML
    html = html.replace("{{PROJECT_COUNT}}", str(count)) # Insère le nombre de projets dans le template HTML

    # Affichage de la liste des utilisateurs inscrits

    user_rows = render_user_rows()
    html = html.replace("{{USER_ROWS}}", user_rows)

    # Affichage des options dans les listes déroulantes

    html = html.replace("{{PROJECT_OPTIONS}}", "\n".join(
        [f'<option value="{p[0]}">{p[1]}</option>' for p in mesProjects()]
    ))

    html = html.replace("{{USER_OPTIONS}}", "\n".join(
        [f'<option value="{u[0]}">{u[1]} {u[2]}</option>' for u in mesUsers()]
    ))

    html = html.replace("{{ROLE_OPTIONS}}", "\n".join(
        [f'<option value="{r[0]}">{r[1]}</option>' for r in mesRoles()]
    ))

    html = html.replace("{{TASK_OPTIONS}}", "\n".join(
        [f'<option value="{t[0]}">{t[1]}</option>' for t in mesTasks()]
    ))

    return html
