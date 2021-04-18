import sys

from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from app.application import Application
from db.db_connection import DatabaseConnectionError

class GuiApplication(Application):
    def __init__(self):
        super().__init__()
    
    def run(self):
        try:
            super().run()
        except DatabaseConnectionError as db_err:
            print(db_err)
            sys.exit(-1)

        
        self._run()

    def _run(self):
        sys.argv += ['--style', 'material']
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.engine.load(QUrl("src/views/MainView.qml"))
        self.app.exec_()
