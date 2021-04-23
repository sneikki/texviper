import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    color: "white"

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
                text: "New project"
                font.pixelSize: 20
            }

            TextField {
                id: name_field
                width: parent.width
                placeholderText: "Name"
            }

            Row {
                width: parent.width
                spacing: 10
                TextField {
                    id: path_field
                    width: 250
                    placeholderText: "Path"
                }
                Button {
                    width: 100
                    text: "Browse"
                }
            }

            Row {
                spacing: 20
                Button {
                    width: 170
                    text: "Cancel"
                    onClicked: create_project_dialog_popup.close()
                }

                Button {
                    width: 170
                    text: "Create"
                    onClicked: home_view.create_project_clicked(name_field.text, path_field.text)
                }
            }
        }
    }
}