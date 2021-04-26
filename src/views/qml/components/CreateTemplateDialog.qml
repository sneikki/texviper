import QtQuick 2.12
import QtQuick.Controls 2.12

Item {
    anchors.left: parent
    anchors.leftMargin: 20
    anchors.right: parent
    anchors.rightMargin: 20
    anchors.top: parent
    anchors.topMargin: 20
    anchors.bottom: parent
    anchors.bottomMargin: 20

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
                width: 250
                placeholderText: 'Path'
            }
            Button {
                width: 100
                text: 'Browse'
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