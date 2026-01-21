import re                                               # Module pour les expressions régulières    
from datetime import datetime                           # Expressions regulières pour validation

# ======== VERIFICATION DES CHAMPS ========

def verifier_user(data):
    
    # Récupère les données
    name, surname, mail = data.get("name"), data.get("surname"), data.get("mail")
    
    # Nettoyage et vérification si les champs sont vides
    name = name.strip() if name else ""
    surname = surname.strip() if surname else ""
    mail = mail.strip() if mail else ""

    if not name or not surname or not mail:
        return False

    # Vérification du format email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", mail):
        return False

    return True

def verifier_projet(data):

    # Récupère les données 
    title, description, begin, end, advance, status, priority = data.get("title"), data.get("description"), data.get("begin"), data.get("end"), data.get("advance"), data.get("status"), data.get("priority") 

    # Nettoyage des textes
    title = title.strip() if title else ""
    description = description.strip() if description else ""
    
    # Vérification des champs obligatoires
    if not title:
        return False
    
    # Vérification de si la date de début est antérieure à la date de fin
    if datetime.strptime(str(begin), "%Y-%m-%d") > datetime.strptime(str(end), "%Y-%m-%d"):
        return False

    # Vérification de la progression (0 à 100)
    if not (0 <= int(advance) <= 100):
        return False

    # Vérification de la priorité (liste autorisée)
    if not str(priority) in ["Critique", "Haute", "Moyenne", "Basse"]:
       return False

    # 6. Vérification du statut (liste autorisée)
    statuts_valides = ["A faire", "En cours", "Terminé", "En attente", "Bloqué"]
    if status not in statuts_valides:
       return False

    return True

def verifier_task(data):

    project, title, description, due_date, status, estimated, done, emergency = data.get("project"), data.get("title"), data.get("description"), data.get("due_date"), data.get("status"), data.get("estimated"), data.get("done"), data.get("emergency") # Récupère les données du dictionnaire data

    # Nettoyage et vérification des champs obligatoires
    title = title.strip() if title else ""
    description = description.strip() if description else ""
    
    if not title or project is None:
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
    if status not in ["A faire", "En cours", "En Attente", "Terminé"]:
        return False

    return True

def verifier_grant(data):
    project_id, user_id, role_id = data.get("project"), data.get("user"), data.get("role") # Récupère les données du dictionnaire data
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
    # On récupère les données
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
    # On récupère les données
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

def checkProject(data):
    return verifier_projet(data) # Vérifie les données du projet avant de l'enregistrer

def checkTask(data):
    return verifier_task(data) # Vérifie les données du task avant de l'enregistrer

def checkUser(data):
    return verifier_user(data) # Vérifie les données de l'utilisateur avant de l'enregistrer

def checkRole(data):
    return True # Pas de vériification spécifique pour les rôles

def saveGrant(data):
    return verifier_grant(data) # Vérifie les données du grant avant de l'enregistrer

# Commenté car uniquement créer / supprimer coté backend

# def saveAlloc(data):
#     #insert("ALLOC", data)
#     return verifier_alloc(data) # Vérifie les données de l'allocation avant de l'enregistrer

# def saveDepend(data):
#     #insert("DEPEND", data)
#     return verifier_depend(data) # Vérifie les données de la dépendance avant de l'enregistrer
