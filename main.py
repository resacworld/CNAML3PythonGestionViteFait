from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import RG
from db import delete_alloc_db, delete_grant_db, delete_project_db, delete_role_db, delete_task_db, delete_user_db, insert
import db

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def root():
    return RG.page_html()


# ================= LISTING =================

@app.get("/projects")
def projects():
    return RG.mesProjects()

@app.get("/tasks")
def tasks():
    print("/tascks called")
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


# ================= CREATE =================

@app.post("/projects/create")
async def create_project(request: Request):
    data = dict(await request.form())
    # if RG.saveProject(data):
    insert("PROJECTS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/tasks/create")
async def create_task(request: Request):
    data = dict(await request.form())
    if RG.saveTask(data):
        insert("TASKS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/users/create")
async def create_user(request: Request):
    data = dict(await request.form())
    if RG.saveUser(data):
        insert("USERS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/roles/create")
async def create_role(request: Request):
    data = dict(await request.form())
    if RG.saveRole(data):
        insert("ROLES", data)
    return RedirectResponse("/", status_code=303)


@app.post("/grants/create")
async def create_grant(request: Request):
    data = dict(await request.form())
    if RG.saveGrant(data):
        insert("GRANTS", data)
    return RedirectResponse("/", status_code=303)


@app.post("/alloc/create")
async def create_alloc(request: Request):
    data = dict(await request.form())
    if RG.saveAlloc(data):
        insert("ALLOC", data)
    return RedirectResponse("/", status_code=303)


@app.post("/depend/create")
async def create_depend(request: Request):
    data = dict(await request.form())
    if RG.saveDepend(data):
        insert("DEPEND", data)
    return RedirectResponse("/", status_code=303)


# ================= EDIT SPECIFIQUE (HTML) =================

@app.get("/projects/edit/{project_id}", response_class=HTMLResponse)
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


@app.post("/projects/delete/{project_id}")
def delete_project(project_id: int):
    db.delete_project_db(project_id)
    return RedirectResponse("/", status_code=303)


# ================= UPDATE SPECIFIQUE (HTML) =================

@app.post("/projects/update/{project_id}")
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


@app.post("/tasks/update")
async def update_task(request: Request):
    data = dict(await request.form())

    task_id = data.pop("number")
    params = {"task": task_id}

    for k, v in data.items():
        if v:
            params[k] = v

    return RG.updateGeneric(params)


# ================= UPDATE GENERIQUE =================

@app.get("/update")
def update(request: Request):
    params = dict(request.query_params)
    return RG.updateGeneric(params)


# ================= SEARCH GENERIQUE =================

@app.get("/search/{query}")
def search(query: str):
    return RG.searchGeneric(query)

# ================= DELETE SPECIFIQUE (DB) =================

@app.post("/projects/delete/{project_id}")
def delete_project(project_id: int):
    delete_project_db(project_id)
    return RedirectResponse("/", status_code=303)

@app.post("/tasks/delete/{task_id}")
def delete_task(task_id: int):
    delete_task_db(task_id)
    return RedirectResponse("/", status_code=303)

@app.post("/users/delete/{user_id}")
def delete_user(user_id: int):
    delete_user_db(user_id)
    return RedirectResponse("/", status_code=303)

@app.post("/roles/delete/{role_id}")
def delete_role(role_id: int):
    delete_role_db(role_id)
    return RedirectResponse("/", status_code=303)

@app.post("/grants/delete/{grant_id}")
def delete_grant(grant_id: int):
    delete_grant_db(grant_id)
    return RedirectResponse("/", status_code=303)

@app.post("/alloc/delete/{alloc_id}")
def delete_alloc(alloc_id: int):
    delete_alloc_db(alloc_id)
    return RedirectResponse("/", status_code=303)

