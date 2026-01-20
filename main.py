from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import RG
import db

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return RG.page_html()


# ================= LISTING =================

@app.get("/projects") # Route pour obtenir la liste des projets
def projects():
    return RG.mesProjects()

@app.get("/tasks") # Route pour obtenir la liste des Tâches
def tasks():
    return RG.mesTasks()

@app.get("/users") # Route pour obtenir la liste des Utilisateurs
def users():
    return RG.mesUsers()

@app.get("/roles") # Route pour obtenir la liste des Rôles
def roles():
    return RG.mesRoles()

@app.get("/grants") # Route pour obtenir la liste des Droits
def grants():
    return RG.mesGrants()

@app.get("/alloc") # Route pour obtenir la liste des Allocations
def alloc():
    return RG.mesAlloc()

@app.get("/depend") # Route pour obtenir la liste des Dépendances
def depend():
    return RG.mesDepend()


# ================= CREATE =================

@app.post("/projects/create") # Route pour créer un nouveau projet 
async def create_project(request: Request):
    data = dict(await request.form())
    # if RG.saveProject(data):
    db.insert("PROJECTS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/tasks/create") # Route pour créer une nouvelle tâche 
async def create_task(request: Request):
    data = dict(await request.form())
    if RG.saveTask(data):
        db.insert("TASKS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/users/create") # Route pour créer un nouvelle utilisateur 
async def create_user(request: Request):
    data = dict(await request.form())
    if RG.saveUser(data):
        db.insert("USERS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/roles/create") # Route pour créer un nouveau rôle
async def create_role(request: Request):
    data = dict(await request.form())
    if RG.saveRole(data):
        db.insert("ROLES", data)
    return RedirectResponse("/", status_code=303)


@app.post("/grants/create") # Route pour créer un nouveau grants
async def create_grant(request: Request):
    data = dict(await request.form())
    if RG.saveGrant(data):
        db.insert("GRANTS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/alloc/create") # Route pour Créer une nouvelle alloc
async def create_alloc(request: Request):
    data = dict(await request.form())
    if RG.saveAlloc(data):
        db.insert("ALLOC", data)
    return RedirectResponse("/", status_code=303)


@app.post("/depend/create") # route pour créer une nouvelle dépendance 
async def create_depend(request: Request):
    data = dict(await request.form())
    if RG.saveDepend(data):
        db.insert("DEPEND", data)
    return RedirectResponse("/", status_code=303)


# ================= EDIT SPECIFIQUE (HTML) =================

@app.get("/projects/edit/{project_id}", response_class=HTMLResponse) # Route pour éditer un projet spécifique *
def edit_project(project_id: int):
    # Récupérer le projet depuis la DB
    projects = db.fetch_all("PROJECTS")
    project_tuple = next((p for p in projects if p[0] == project_id), None)

    if not project_tuple:
        return HTMLResponse(f"<h1>Projet {project_id} introuvable</h1>", status_code=404)

    # Transformer le tuple en dictionnaire
    project = {
        "id": project_tuple[0],
        "title": project_tuple[1],
        "description": project_tuple[2],
        "begin": project_tuple[3],
        "end": project_tuple[4],
        "advance": project_tuple[5],
        "status": project_tuple[6],
        "priority": project_tuple[7],
    }

    # Générer la page HTML
    return RG.page_html(mode="edit", project=project)


# ================= UPDATE SPECIFIQUE (HTML) =================

@app.post("/projects/update/{project_id}") # Route pour mettre à jour un projet spécifique
async def update_project(project_id: int, request: Request):
    data = dict(await request.form())

    # Nettoyage : enlever les champs vides
    clean_data = {k: v for k, v in data.items() if v != ""}

    # Mise à jour
    db.update("PROJECTS", project_id, clean_data)

    return RedirectResponse("/", status_code=303)


# @app.post("/projects/update")
# async def update_project(request: Request):
#     data = dict(await request.form())

#     project_id = data.pop("number")
#     params = {"project": project_id}

#     for k, v in data.items():
#         if v:
#             params[k] = v

#     return RG.updateGeneric(params)


@app.post("/tasks/update") # Route pour mettre à jour une tâche spécifique
async def update_task(request: Request):
    data = dict(await request.form())

    task_id = data.pop("number")
    params = {"task": task_id}

    for k, v in data.items():
        if v:
            params[k] = v

    return RG.updateGeneric(params) # utilisation de la fonction générique 


# ================= UPDATE GENERIQUE =================

@app.get("/update") # Route pour la mise à jour générique
def update(request: Request):
    params = dict(request.query_params)
    return RG.updateGeneric(params)


# ================= SEARCH GENERIQUE =================

@app.get("/search/{query}") # Route pour la recherche générique 
def search(query: str):
    return RG.searchGeneric(query)

# ================= DELETE SPECIFIQUE (DB) =================

@app.post("/projects/delete/{project_id}") # Route pout supprimer un projet spécifique
def delete_project(project_id: int):
    db.delete_project_db(project_id)
    return RedirectResponse("/", status_code=303)

@app.post("/tasks/delete/{task_id}") # route pour supprimer une tâche spécifique
def delete_task(task_id: int):
    db.delete_task_db(task_id)
    return RedirectResponse("/", status_code=303)

@app.post("/users/delete/{user_id}") # route pour supprimer un utilisateur spécifique
def delete_user(user_id: int):
    db.delete_user_db(user_id)
    return RedirectResponse("/", status_code=303)

@app.post("/roles/delete/{role_id}") # route pour supprimer un rôle spécifique
def delete_role(role_id: int):
    db.delete_role_db(role_id)
    return RedirectResponse("/", status_code=303)

@app.post("/grants/delete/{grant_id}") # route pour supprimer un droit spécifique
def delete_grant(grant_id: int):
    db.delete_grant_db(grant_id)
    return RedirectResponse("/", status_code=303)

@app.post("/alloc/delete/{alloc_id}") # route pour supprimer une alloc spécifique 
def delete_alloc(alloc_id: int):
    db.delete_alloc_db(alloc_id)
    return RedirectResponse("/", status_code=303)

