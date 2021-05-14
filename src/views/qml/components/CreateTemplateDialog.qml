import QtQuick 2.12
import QtQuick.Controls 2.12

Item {
    onVisibleChanged: {
        if (visible) {
            pathField.text = template_view.get_default_path()
        }
    }

    Column {
        width: 360
        spacing: 20

        Text {
            text: 'New template'
            font.pixelSize: 20
        }

        TextField {
            id: nameField
            width: parent.width
            placeholderText: 'Name'
        }

        TextField {
            id: filenameField
            width: parent.width
            placeholderText: 'Filename'
        }

        Row {
            width: parent.width
            spacing: 10
            TextField {
                id: pathField
                width: parent.width
                placeholderText: 'Path'
            }
        }

        Row {
            spacing: 20
            Button {
                width: 170
                text: 'Cancel'
                onClicked: createTemplateDialog.close()
            }

            Button {
                width: 170
                text: 'Create'
                onClicked: {
                    template_view.create_template_clicked(nameField.text, filenameField.text, pathField.text)
                    nameField.text = ''
                    filenameField.text = ''
                    pathField.text = ''
                    createTemplateDialog.close()
                }
            }
        }
    }
}
