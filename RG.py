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

def saveProject(data):
    insert("PROJECTS", data)
    return {"status": "Projet enregistré"}

def saveTask(data):
    insert("TASKS", data)
    return {"status": "Tâche enregistrée"}

def saveUser(data):
    insert("USERS", data)
    return {"status": "Utilisateur enregistré"}

def saveRole(data):
    insert("ROLES", data)
    return {"status": "Rôle enregistré"}

def saveGrant(data):
    insert("GRANTS", data)
    return {"status": "Grant enregistré"}

def saveAlloc(data):
    insert("ALLOC", data)
    return {"status": "Allocation enregistrée"}

def saveDepend(data):
    insert("DEPEND", data)
    return {"status": "Dépendance enregistrée"}


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
                insert(table, params)
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
