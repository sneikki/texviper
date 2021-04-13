import sys

from controllers.project_controller import project_controller
from stores.project_store import CreateProjectError

def main(args):
    if '--cli' in args[1:]:
        print("Running cli")
    else:
        print("Running gui")

    path = input("Project location: ")
    name = input("Project name: ")

    try:
        project_controller.create_project(name, path)
    except CreateProjectError as e:
        print("Unable to create project: " + str(e))
    else:
        print("Created project " + name + " at " + path)

if __name__ == '__main__':
    main(sys.argv)
