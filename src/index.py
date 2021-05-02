import sys

from app.cli_application import CliApplication
from app.gui_application import GuiApplication


def get_mode(param):
    if param == '--cli':
        return 'cli'
    else:
        return 'gui'


if __name__ == '__main__':
    mode = get_mode(sys.argv[1])

    if mode == 'cli':
        app = CliApplication()
    else:
        app = GuiApplication()

    app.run()
