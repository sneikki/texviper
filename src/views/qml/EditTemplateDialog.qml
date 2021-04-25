import QtQuick 2.12
import QtQuick.Controls 2.12

Item {
        id: item1
        anchors.left: parent.left
        anchors.leftMargin: 20
        anchors.right: parent.right
        anchors.rightMargin: 20
        anchors.top: parent.top
        anchors.topMargin: 20
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20

        Text {
            id: templateTitle
            x: 0
            y: 0
            text: "Edit template"
            font.pixelSize: 20
        }

        Row {
            id: buttons
            x: 0
            y: 264
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.bottomMargin: 0
            spacing: 20
            Button {
                width: parent.width / 2 - 10
                text: "Cancel"
                onClicked: editTemplateDialog.close()
            }

            Button {
                width: parent.width / 2 - 10
                text: "Save"
                onClicked: {
                    template_view.save_clicked(editTemplateDialogContent.text)
                    editTemplateDialog.close()
                }
            }
        }

        Rectangle {
            id: textEditWrapper
            color: "#e1e1e1"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: templateTitle.bottom
            anchors.bottom: buttons.top
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.topMargin: 50
            anchors.bottomMargin: 50

            ScrollView {
                id: scrollView
                anchors.fill: parent
                clip: true

                TextEdit {
                    objectName: "editTemplateDialogContent"
                    id: editTemplateDialogContent
                    color: "#666666"
                    text: "jdskjdskd"
                    anchors.fill: parent
                    font.pixelSize: 12
                    wrapMode: Text.WrapAnywhere
                    selectionColor: "#9b9b9b"
                    font.family: "Source Code Pro"
                    padding: 25
                    selectByMouse: true
                }
            }
        }
    }