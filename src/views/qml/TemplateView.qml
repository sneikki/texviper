import QtQuick 2.12
import QtQuick.Controls 2.12

Item {
    width: parent.width
    height: parent.height

    Text {
        id: templatesTitle
        text: "Templates"
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 50
        anchors.topMargin: 50
        font.pixelSize: 20
        color: "#999999"
    }

    ScrollView {
        id: templatesList
        anchors.right: parent.right
        anchors.rightMargin: 50
        anchors.left: parent.left
        anchors.top: templatesTitle.bottom
        anchors.leftMargin: 50
        anchors.topMargin: 50
        height: window.height - 300
        clip: true

        Column {
            objectName: "templatesListColumn"
            id: templatesColumnList
            width: parent.width
            height: parent.height
            spacing: 20
        }
    }

    Button {
        id: addTemplateButton
        text: "Add template"
        anchors.left: parent.left
        anchors.top: templatesList.bottom
        anchors.topMargin: 50
        anchors.leftMargin: 50
        onClicked: createTemplateDialog.open()
    }

    Popup {
        id: createTemplateDialog
        width: 400
        height: 330
        x: Math.round((window.width - width) / 2)
        y: Math.round((window.height - height) / 2)
        padding: 20
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

        CreateTemplateDialog {

        }
    }

    Popup {
        objectName: "editTemplateDialog"
        id: editTemplateDialog
        width: window.width - 200
        height: window.height - 200
        x: 100
        y: 100
        padding: 20
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

        EditTemplateDialog {
            
        }
    }
}
