from PySide2.QtCore import QObject, Slot
from PySide2.QtQuick import QQuickItem
from PySide2.QtQml import QQmlComponent

from views.view import View
from controllers.template_controller import template_controller
from stores.template_store import template_store
from utils.exceptions import InvalidValueError
from utils.literal import get_literal
from config.config import config

class TemplateView(View):
    def __init__(self, engine):
        super().__init__(engine)

        self.component = QQmlComponent(self.engine)
        self.component.loadUrl('src/views/qml/components/TemplateListItem.qml')
        self.templates_list = self.root.findChild(
            QQuickItem, 'templatesListColumn')
        self.load_templates()
        self.current = None

    def load_templates(self):
        """ Loads all existing templates and creates ui
            entries for them.
        """
        templates = template_controller.get_templates()

        for template in templates:
            self.add_template(template)

    def add_template(self, template):
        """ Creates a ui entry for single template
        """
        item = self.component.create()
        item.setProperty('name', template.name)
        item.setProperty('template_id', template.template_id)
        item.setObjectName(template.template_id)
        item.setParentItem(self.templates_list)
        item.setParent(self.templates_list)

    @Slot(str, str, str)
    def create_template_clicked(self, name, filename, path):
        """ Called when new template button is clicked.
            Creates a new template.

            Args:
                name (string): Name of the template, entered by user
                filename (string): File name of the template entered by user
                path (string): Path of the template, entered by user
        """
        try:
            template = template_controller.create_template(
                name, filename, path, '')
            self.add_template(template)
        except PermissionError:
            self.show_error(get_literal('template_creation_failed'), get_literal('permission_denied'))
        except FileExistsError:
            self.show_error(get_literal('template_already_exists'), get_literal('permission_denied'))
        except InvalidValueError as err:
            self.show_error(get_literal('template_creation_failed'), str(err))

    @Slot(str)
    def remove_template(self, template_id):
        """ Called when remove button is clicked on a template
            Removes the template

            Args:
                template_id (string): Id of the template to remove
        """
        template_controller.remove_template(template_id)

        obj = self.root.findChild(QQuickItem, template_id)
        obj.deleteLater()

    @Slot(str)
    def edit_clicked(self, template_id):
        """ Called when edit button is clicked on a template
            Opens template editing view.

        Args:
            template_id (string): Id of the template to open
                the edit view for
        """
        source = template_controller.get_source(template_id)
        child = self.root.findChild(QObject, 'editTemplateDialog')
        child.setProperty('visible', True)

        child = self.root.findChild(QObject, 'editTemplateDialogContent')
        child.setProperty('text', source)

        self.current = template_id

    @Slot(str)
    def save_clicked(self, source):
        """ Called when save button is clicked. Saves the
            template being edited currently.

            Args:
                source (string): Source of the template to save
        """
        template_store.write(self.current, source)

    @Slot(result=str)
    def get_default_path(self):
        """ Returns default path where templates shall be saved

            Returns:
                string: Default path
        """
        return config.get_value('default_template_path')
