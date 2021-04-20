from controllers.project_controller import project_controller
from utils.exceptions import DirectoryNotEmptyError, ProjectExistsError
from sqlite3 import IntegrityError

def run():
    projects = project_controller.get_project_names()
    print("\n".join(projects))

    path = "~/test"
    name = input("Enter project name: ")

    try:
        project_controller.remove_project(name)
        # project_controller.create_project(name, path)
    except PermissionError:
        print("Unable to create project: insufficient permissions")
    except IntegrityError:
        print("Unable to create project: invalid data")
    except DirectoryNotEmptyError:
        print("Unable to create project: directory not empty")
    except ProjectExistsError:
        print(f"Unable to create project: project {name} already exists")
