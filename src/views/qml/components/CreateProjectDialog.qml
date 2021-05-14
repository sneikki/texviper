import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    color: 'white'
    onVisibleChanged: {
        if (visible) {
            path_field.text = home_view.get_default_path()
        }
    }

    Item {
        Column {
            width: 360
            spacing: 20

            Text {
                text: 'New project'
                font.pixelSize: 20
            }

            TextField {
                id: name_field
                width: parent.width
                placeholderText: 'Name'
            }

            Row {
                width: parent.width
                spacing: 10
                TextField {
                    id: path_field
                    width: parent.width
                    placeholderText: 'Path'
                }
            }

            Column {
                width: parent.width
                spacing: 5

                Text {
                    width: parent.width
                    text: 'Template'
                }

                ComboBox {
                    id: templateDropdown
                    objectName: 'templateDropdown'
                    width: parent.width
                    model: []

                    function set_model(m) {
                        model = m
                    }
                }
            }

            Row {
                spacing: 20
                Button {
                    width: 170
                    text: 'Cancel'
                    onClicked: create_project_dialog_popup.close()
                }

                Button {
                    width: 170
                    text: 'Create'
                    onClicked: {
                        home_view.create_project_clicked(name_field.text, path_field.text, templateDropdown.currentText)
                        name_field.text = ''
                        path_field.text = ''
                        templateDropdown.currentIndex = 0
                        create_project_dialog_popup.close()
                    }
                }
            }
        }
    }
}
