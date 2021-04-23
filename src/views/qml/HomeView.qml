import QtQuick 2.12
import QtQuick.Controls 2.12

Item {
    width: parent.width
    height: parent.height

    Item {
        id: header
        width: parent.width
        height: 100

        clip: true
        Rectangle {
                id: rectangle
                color: "#ffffff"
                anchors.fill: parent
                anchors.topMargin: -1
                anchors.rightMargin: -1
                anchors.leftMargin: -1
                border.color: "#ddd"
            }

        Row {
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 36
                spacing: 36
                Button {
                    text: qsTr("Import project")
                    onClicked: home_view.import_project_clicked()
                }

                Button {
                    text: qsTr("Create new project")
                    onClicked: create_project_dialog_popup.open()
                }
        }
    }

    Item {
        id: body
        width: parent.width
        anchors.top: parent.top
        anchors.bottomMargin: 0
        anchors.bottom: parent.bottom
        anchors.topMargin: 100

        Grid {
            objectName: "projects"
            id: "projects"
            anchors.fill: window
            spacing: 25
        }
    }

    Popup {
        id: create_project_dialog_popup
        width: 400
        height: 280
        x: Math.round((window.width - width) / 2)
        y: Math.round((window.height - height) / 2)
        padding: 20
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

        CreateProjectDialog {
        }
    }
}
