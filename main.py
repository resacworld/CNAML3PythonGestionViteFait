from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from db import init_db   # Fonction de gestion de la BDD
import RG, db, render

init_db()

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    """
    Route principale affichant la page d'accueil avec les listes des projets, tâches, utilisateurs, rôles, droits, allocations et dépendances
    """

    return render.page_html()

# ================= CREATES =================

@app.post("/projects/create")
async def create_project(request: Request):
    """
    Route pour créer un nouveau projet 
    """

    data = dict(await request.form())
    if RG.checkProject(data):
        db.insert("PROJECTS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/tasks/create")
async def create_task(request: Request):
    """
    Route pour créer une nouvelle tâche 
    """

    data = dict(await request.form())
    if RG.checkTask(data):
        db.insert("TASKS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/users/create")
async def create_user(request: Request):
    """
    Route pour créer un nouvelle utilisateur 
    """

    data = dict(await request.form())
    if RG.checkUser(data):
        db.insert("USERS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/roles/create")
async def create_role(request: Request):
    """
    Route pour créer un nouveau rôle
    """

    data = dict(await request.form())
    if RG.checkRole(data):
        db.insert("ROLES", data)
    return RedirectResponse("/", status_code=303)


@app.post("/grants/create")
async def create_grant(request: Request):
    """
    Route pour créer un nouveau grants
    """

    data = dict(await request.form())
    if RG.saveGrant(data):
        db.insert("GRANTS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/depend/create")
async def create_depend(request: Request):
    """
    Route pour créer une nouvelle dépendance entre les taĉhes
    """

    data = dict(await request.form())
    if RG.saveDepend(data):
        db.insert("DEPEND", data)
    return RedirectResponse("/", status_code=303)


# ================= UPDATES =================

@app.get("/projects/update/{project_id}", response_class=HTMLResponse)
def edit_project(project_id: int):
    """
    Route pour éditer un projet spécifique
    """

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

    return render.page_html()

@app.post("/projects/update/{project_id}")
async def update_project(project_id: int, request: Request):
    """
    Route pour mettre à jour un projet spécifique
    """
    data = dict(await request.form())

    # Nettoyage : enlever les champs vides
    clean_data = {k: v for k, v in data.items() if v != ""}

    # Mise à jour
    db.update("PROJECTS", project_id, clean_data)

    return RedirectResponse("/", status_code=303)


@app.post("/tasks/update/{task_id}", response_class=HTMLResponse)
async def update_task(task_id: int, request: Request):
    """
    Route pour mettre à jour une tâche spécifique
    """
    data = dict(await request.form())

    clean_data = {k: v for k, v in data.items() if v != ""}

    # Mise a jour de la dépendance si necessaire
    depend = clean_data.get("depend")
    if depend is not None:
        db.set_task_depend(task_id, depend)
        clean_data.pop("depend")
    else:
        db.remove_all_task_depend(task_id)

    # Mise a jour de l'assignment si necessaire
    person = clean_data.get("person")
    if person is not None:
        db.set_task_person(task_id, person)
        clean_data.pop("person")
    else:
        db.remove_task_person(task_id)

    db.update("TASKS", task_id, clean_data)

    return render.page_html()

# ================= DELETES =================

@app.post("/projects/delete/{project_id}")
def delete_project(project_id: int):
    """
    Route pout supprimer un projet spécifique
    """
    db.delete_project_db(project_id)
    return RedirectResponse("/", status_code=303)

@app.post("/tasks/delete/{task_id}")
def delete_task(task_id: int):
    """
    route pour supprimer une tâche spécifique
    """
    db.delete_task_db(task_id)
    return RedirectResponse("/", status_code=303)

@app.post("/users/delete/{user_id}")
def delete_user(user_id: int):
    """
    route pour supprimer un utilisateur spécifique
    """
    db.delete_user_db(user_id)
    return RedirectResponse("/", status_code=303)

@app.post("/roles/delete/{role_id}")
def delete_role(role_id: int):
    """
    route pour supprimer un rôle spécifique
    """
    db.delete_role_db(role_id)
    return RedirectResponse("/", status_code=303)

@app.post("/grants/delete/")
async def delete_grant(request: Request):
    """
    route pour supprimer un droit spécifique
    """

    data = dict(await request.form())

    project_id, user_id = data.get("project"), data.get("user")

    db.delete_grant_db(project_id, user_id)
    return RedirectResponse("/", status_code=303)

@app.post("/alloc/delete/{alloc_id}")
def delete_alloc(alloc_id: int):
    """
    route pour supprimer une alloc spécifique 
    """
    db.delete_alloc_db(alloc_id)
    return RedirectResponse("/", status_code=303)

