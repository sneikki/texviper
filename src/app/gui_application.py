import sys

from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

from app.application import Application
from db.db_connection import DatabaseConnectionError

from views.root_view import RootView
from views.home_view import HomeView
from views.project_view import ProjectView
from views.settings_view import SettingsView
from views.template_view import TemplateView

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
        self._initialize()
        

        root_view = RootView()
        self.add_view('root_view', root_view)
        home_view = HomeView(self.engine)
        self.add_view('home_view', home_view)
        settings_view = SettingsView(self.engine)
        self.add_view('settings_view', settings_view)
        project_view = ProjectView()
        self.add_view('project_view', project_view)
        template_view = TemplateView(self.engine)
        self.add_view('template_view', template_view)

        self.app.exec_()

    def _initialize(self):
        # This may not be the most elegant way to enable
        # Material, but there does not seem any other way
        sys.argv += ['--style', 'material']
        self.app = QGuiApplication(sys.argv)
        self.engine = QQmlApplicationEngine()


        self.engine.load(QUrl('src/views/qml/RootView.qml'))
        # self.app.exec_()

    def add_view(self, name, view):
        self.engine.rootContext().setContextProperty(name, view)
        view.engine = self.engine
