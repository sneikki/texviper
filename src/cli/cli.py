from controllers.project_controller import project_controller
from utils.exceptions import DirectoryNotEmptyError, ProjectExistsError
from sqlite3 import IntegrityError

def run():

    while True:
        print("#### Projects ####")
        print('\n'.join(
            list(
                map(
                    lambda n: f"* {n}",
                    project_controller.get_project_names()
                )
            )
        ))

        print('1. Create new project\n2. Remove existing project\n3. Add resource to project\n4. Quit')
        choice = input()

        if choice == "1":
            name = input('Project name: ')
            path = input('Project location: ')

            project_controller.create_project(name, path)

            print(f"Created project {name} at {path}")
        elif choice == "2":
            name = input('Project name: ')

            project = project_controller.get_project_by_name(name)
            project_controller.remove_project(project.project_id)

            print(f"Removed project {name}")
        elif choice == "3":
            project_name = input("Project name: ")
            name = input("Resource name: ")
            path = input("Resource location in project: ")
            resource_type = input("Resource type: ")

            project = project_controller.get_project_by_name(project_name)

            project_controller.add_resource(name, path, resource_type, project.project_id)
        
            print(f"Added {name} to {project_name}")
        else:
            break
