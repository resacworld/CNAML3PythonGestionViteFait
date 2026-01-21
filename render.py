import db

def pers_assigneed_to_project(project_id):
    """
    Récupère les personnes assignées à un projet donné
    """

    grants = db.fetch_all("GRANTS")
    users = db.fetch_all("USERS")

    assigned_users = []
    for g in grants:
        grant_project_id = g[1]
        user_id = g[2]

        if grant_project_id == project_id:
            user = next((u for u in users if u[0] == user_id), None)
            role_of_user = db.fetch_by_id("ROLES", g[3])[1]
            if user:
                assigned_users.append(f"{user[1]} {user[2]} ({role_of_user})") # Nom et prénom

    return ", ".join(assigned_users) if assigned_users else "Aucun"

def render_projects_rows(): 
    """
    Génère les lignes HTML pour la liste des projets
    """

    projects = db.fetch_all("PROJECTS")
    rows = []

    for p in projects:
        number   = p[0]  # identifiant
        title    = p[1]  # titre
        desc     = p[2]  # description
        begin    = p[3]  # date début
        end      = p[4]  # date fin
        advance  = p[5]  # 0 à 100
        status   = p[6]  # en cours, terminé, en attente, bloqué, à faire
        priority = p[7]  # Critique, haute, moyenne, basse

        rows.append(f"""
<tr>
    <td colspan="8" style="padding:0;">
        <details class="project-details">
            <summary>
                <table style="width:100%; border-collapse:collapse;">
                    <tr>
                        <form action="/projects/update/{number}" method="POST">
                            <td style="font-weight:600; width:50px;">{number}</td>

                            <td style="width: 20%;">
                                <input type="text" name="title" value="{title}" onchange="this.form.submit()" required style="width:100%; border:none; font-weight:600;">
                                <br>
                                <textarea name="description" rows="2" onchange="this.form.submit()" style="width:100%; border:none; resize:none;">{desc}</textarea>
                            </td>

                            <td style="width: 13%;">
                                <select name="status" onchange="this.form.submit()">
                                    <option value="A faire" {"selected" if status == "A faire" else ""}>A faire</option>
                                    <option value="En cours" {"selected" if status == "En cours" else ""}>En cours</option>
                                    <option value="Terminé" {"selected" if status == "Terminé" else ""}>Terminé</option>
                                    <option value="En attente" {"selected" if status == "En attente" else ""}>En attente</option>
                                    <option value="Bloqué" {"selected" if status == "Bloqué" else ""}>Bloqué</option>
                                </select>
                            </td>

                            <td style="width: 150px;">
                                <input type="number" name="advance" value="{advance}" min="0" max="100" onchange="this.form.submit()">
                                <div class="progress" style="margin-top:4px;">
                                    <div class="progress-bar" style="width:{advance}%;">{advance}%</div>
                                </div>
                            </td>

                            <td style="width: 13%;">
                                <select name="priority" onchange="this.form.submit()">
                                    <option value="Critique" {"selected" if priority == "Critique" else ""}>Critique</option>
                                    <option value="Haute" {"selected" if priority == "Haute" else ""}>Haute</option>
                                    <option value="Moyenne" {"selected" if priority == "Moyenne" else ""}>Moyenne</option>
                                    <option value="Basse" {"selected" if priority == "Basse" else ""}>Basse</option>
                                </select>
                            </td>

                            <td style="width: 16%;"><input type="date" name="end" value="{end}" onchange="this.form.submit()"></td>

                            <td style="width: auto;">
                                {pers_assigneed_to_project(number)}
                            </td>
                        </form>

                            <td style="white-space:nowrap; width:140px; text-align:center;">
                                <!--a href="/projects/update/{number}" title="Modifier" style="margin-right:8px;">✏️</a-->
                                <form action="/projects/delete/{number}" method="POST" style="display:inline;" onsubmit="return confirm('Êtes-vous sûr de vouloir supprimer ce projet ?');">
                                    <button type="submit" style="background:none; border:none; color:#ef4444; cursor:pointer;"><i class="fas fa-trash"></i></button>
                                </form>
                            </td>
                    </tr>
                </table>
            </summary>

            <!-- TÂCHES DU PROJET -->
            <div class="tasks-box">
                {render_tasks(number)}
            </div>
        </details>
    </td>
</tr>
""")
    return "\n".join(rows), len(projects)


def render_tasks(project_id):
    """
    Genère les lignes HTML pour la liste des tâches d'un projet donné
    """

    tasks = db.fetch_tasks_for_project(project_id)

    if not tasks:
        return "<em>Aucune tâche liée à ce projet</em>"

    rows = ""
    for t in tasks:
        other_tasks = []
        selected_depend = db.get_task_depend(t[0])
        alloc = db.get_task_person(t[0])

        persons = "\n".join(
        [   f'<option value="{u[0]}" {"selected" if u[0] == alloc else ""}>{u[1]} {u[2]}</option>' for u in db.mesUsers()]
        )

        for task in tasks:
            if task[0] != t[0]:
                other_tasks.append(f"""<option value="{task[0]}" {"selected" if selected_depend == task[0] else ""}>{task[1]}</option>""") 


        rows += f"""
        <tr>
            <form action="/tasks/update/{t[0]}" method="POST">
                <td>{t[0]}</td>
                <td><input type="text" name="title" value="{t[1]}" onchange="this.form.submit()" required></td>
                <td>
                    <select name="status" onchange="this.form.submit()">
                        <option value="A faire" {"selected" if t[2] == "A faire" else ""}>A faire</option>
                        <option value="En cours" {"selected" if t[2] == "En cours" else ""}>En cours</option>
                        <option value="En Attente" {"selected" if t[2] == "En Attente" else ""}>En Attente</option>
                        <option value="Terminé" {"selected" if t[2] == "Terminé" else ""}>Terminé</option>
                    </select>
                </td>
                <td><input type="date" name="due_date" value={t[3]} onchange="this.form.submit()" required></td>
                <td>
                    <select name="depend" onchange="this.form.submit()">
                        <option value="">Aucune</option>
                        {other_tasks}
                    </select>
                </td>
                <td>
                    <select name="person" onchange="this.form.submit()">
                        <option value="">Aucune</option>
                        {persons}
                    </select>
                </td>
            </form>
            <form action="/tasks/delete/{t[0]}" method="POST" onsubmit="return confirm('Supprimer cette tâche ?');">
                <td style="text-align:center;">
                    <button type="submit"
                            style="background:none; border:none; color:#ef4444; cursor:pointer;">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </form>
        </tr>
        """

    return f"""
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Tâche</th>
          <th>Statut</th>
          <th>Date limite</th>
          <th>Dépend de</th>
          <th>Personne</th>
          <th>Supprimer</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
    """

def render_user_rows():
    """
    Génère les lignes HTML pour la liste des utilisateurs
    """

    users = db.fetch_all("USERS")

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




def page_html():
    """
    Retoure la page html en fonction du mode (main ou edit) et des données du projet si en mode edit
    + Remplace les placeholders dans le template HTML par les valeurs réelles
    """

    html = open("templates/dashboard.html").read() 

    project_rows, count = render_projects_rows()            # Génère les lignes HTML pour la liste des projets
    html = html.replace("{{PROJECT_ROWS}}", project_rows)   # Insère les lignes dans le template HTML
    html = html.replace("{{PROJECT_COUNT}}", str(count))    # Insère le nombre de projets dans le template HTML

    # Affichage de la liste des utilisateurs inscrits
    user_rows = render_user_rows()
    html = html.replace("{{USER_ROWS}}", user_rows)

    # Affichage des options dans les listes déroulantes
    html = html.replace("{{PROJECT_OPTIONS}}", "\n".join(
        [f'<option value="{p[0]}">{p[1]}</option>' for p in db.mesProjects()]
    ))  # Remplace les options des projets

    html = html.replace("{{USER_OPTIONS}}", "\n".join(
        [f'<option value="{u[0]}">{u[1]} {u[2]}</option>' for u in db.mesUsers()]
    )) # Remplace les options des utilisateurs

    html = html.replace("{{ROLE_OPTIONS}}", "\n".join(
        [f'<option value="{r[0]}">{r[1]}</option>' for r in db.mesRoles()]
    ))  # Remplace les options des rôles

    html = html.replace("{{TASK_OPTIONS}}", "\n".join(
        [f'<option value="{t[0]}">{t[1]}</option>' for t in db.mesTasks()]
    ))  # Remplace les options des tâches

    return html