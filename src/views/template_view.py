from PySide2.QtCore import QObject, Slot
from PySide2.QtQuick import QQuickItem
from PySide2.QtQml import QQmlComponent

from controllers.template_controller import template_controller
from stores.template_store import template_store
from utils.exceptions import InvalidValueError

class TemplateView(QObject):
    def __init__(self, engine):
        super().__init__()

        self.engine = engine
        self.root = self.engine.rootObjects()[0]

        self.component = QQmlComponent(self.engine)
        self.component.loadUrl('src/views/qml/TemplateListItem.qml')        
        self.templates_list = self.root.findChild(QQuickItem, 'templatesListColumn')
        self.load_templates()
        self.current = None


    def load_templates(self):
        templates = template_controller.get_templates()
        
        for template in templates:
            self.add_template(template)

    def add_template(self, template):
        item = self.component.create()
        item.setProperty('name', template.name)
        item.setProperty('template_id', template.template_id)
        item.setObjectName(template.template_id)
        item.setParentItem(self.templates_list)
        item.setParent(self.templates_list)

    @Slot(str, str, str)
    def create_template_clicked(self, name, filename, path):

        try:
            template = template_controller.create_template(name, filename, path, '')
            self.add_template(template)
        except PermissionError:
            print("Unable to create template: permission denied")
        except FileExistsError:
            print("Unable to create template: template exists")
        except InvalidValueError as err:
            print(err)

    @Slot(str)
    def remove_template(self, template_id):
        template_controller.remove_template(template_id)

        obj = self.root.findChild(QQuickItem, template_id)
        obj.deleteLater()

    @Slot(str)
    def edit_clicked(self, template_id):
        source = template_controller.get_source(template_id)
        child = self.root.findChild(QObject, "editTemplateDialog")
        child.setProperty("visible", True)

        child = self.root.findChild(QObject, "editTemplateDialogContent")
        child.setProperty("text", source)
        
        self.current = template_id

    @Slot(str)
    def save_clicked(self, source):
        template_store.write(self.current, source)
