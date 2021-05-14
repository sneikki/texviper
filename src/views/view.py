from PySide2.QtCore import QObject

class View(QObject):
    def __init__(self, engine):
        super().__init__()

        self.engine = engine
        self.root = self.engine.rootObjects()[0]

    def show_error(self, title, message):
        """ Shows a general error message dialog

        Args:
            title (string): Title of the error dialog
            message (string): Message of the error dialog
        """
        error_dialog = self.root.findChild(QObject, 'errorDialog')
        error_dialog.setProperty('title', title)
        error_dialog.setProperty('text', message)
        error_dialog.setProperty('visible', True)
