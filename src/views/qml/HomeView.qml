import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Dialogs 1.1
import 'components'

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
                color: '#ffffff'
                anchors.fill: parent
                anchors.topMargin: -1
                anchors.rightMargin: -1
                anchors.leftMargin: -1
                border.color: '#ddd'
            }

        Row {
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 36
                spacing: 36
                Button {
                    text: qsTr('Import project')
                    onClicked: home_view.import_project_clicked()
                }

                Button {
                    text: qsTr('Create new project')
                    onClicked: {
                        home_view.load_templates()
                        create_project_dialog_popup.open()
                    }
                }
        }
    }

    Item {
        id: body
        width: parent.width
        anchors.top: header.bottom
        anchors.bottomMargin: 0
        anchors.bottom: parent.bottom
        anchors.topMargin: 0

        ScrollView {
            width: parent.width
            height: window.height - 155
            clip: true

            Grid {
                id: projects
                objectName: 'projects'
                width: window.width - 25
                height: parent.height - 25
                x: 25
                y: 25
                spacing: 25

                onWidthChanged: {
                    var c = Math.floor(projects.width / 225)
                    projects.columns = c
                }
            }
        }
    }

    Popup {
        id: create_project_dialog_popup
        width: 400
        height: 350
        x: Math.round((window.width - width) / 2)
        y: Math.round((window.height - height) / 2)
        padding: 20
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

        CreateProjectDialog {
        }
    }

    MessageDialog {
        id: confirmRemovalDialog
        objectName: 'confirmRemovalDialog'
        title: 'Remove project'
        text: 'Confirm project removal'
        standardButtons: StandardButton.Cancel | StandardButton.Yes
        onYes: {
            var id = home_view.remove_confirmed()
            project_view.close_project(id)
        }
    }

    MessageDialog {
        id: errorDialog
        objectName: 'errorDialog'
        standardButtons: StandardButton.Ok
        onAccepted: {
            errorDialog.close()
        }
    }
}
