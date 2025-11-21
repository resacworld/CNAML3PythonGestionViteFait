from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import RG

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
    RG.saveProject(data)
    return RedirectResponse("/", status_code=303)


@app.post("/tasks/create")
async def create_task(request: Request):
    data = dict(await request.form())
    RG.saveTask(data)
    return RedirectResponse("/", status_code=303)


@app.post("/users/create")
async def create_user(request: Request):
    data = dict(await request.form())
    RG.saveUser(data)
    return RedirectResponse("/", status_code=303)


@app.post("/roles/create")
async def create_role(request: Request):
    data = dict(await request.form())
    RG.saveRole(data)
    return RedirectResponse("/", status_code=303)


@app.post("/grants/create")
async def create_grant(request: Request):
    data = dict(await request.form())
    RG.saveGrant(data)
    return RedirectResponse("/", status_code=303)


@app.post("/alloc/create")
async def create_alloc(request: Request):
    data = dict(await request.form())
    RG.saveAlloc(data)
    return RedirectResponse("/", status_code=303)


@app.post("/depend/create")
async def create_depend(request: Request):
    data = dict(await request.form())
    RG.saveDepend(data)
    return RedirectResponse("/", status_code=303)


# ================= UPDATE SPECIFIQUE (HTML) =================

@app.post("/projects/update")
async def update_project(request: Request):
    data = dict(await request.form())

    project_id = data.pop("number")
    params = {"project": project_id}

    for k, v in data.items():
        if v:
            params[k] = v

    return RG.updateGeneric(params)


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

