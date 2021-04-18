from controllers.project_controller import project_controller
from stores.project_store           import CreateProjectError
from utils.literal                  import literals

def run():
    while True:
        projects = map(lambda p: f"""* {p}""", project_controller.get_project_names())

        print_projects(projects)

        print(
            """Options:
1. Create new project
2. Remove existing project
3. Quit"""
        )

        action = int(input())
        if action == 1:
            create_project()
        elif action == 2:
            remove_project()
        elif action == 3:
            break

def print_projects(projects):
    project_list = '\n'.join(projects)
    print(
        f"""********
Projects
********

{project_list}
"""
    )

def create_project():
    name = input("Project name: ")
    path = input("Project path: ")
    try:
        project_controller.create_project(name, path)
    except CreateProjectError as e:
        print(f"{literals['project_creation_failed']}: {e}")
    else:
        print(f"{literals['project_created']} {name}")

def remove_project():
    name = input("Project name: ")

    project_controller.remove_project(name)
