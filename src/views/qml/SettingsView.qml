import QtQuick 2.12
import QtQuick.Controls 2.12

Item {
    width: parent.width
    height: parent.height

    ScrollView {
        x: 25
        y: 76
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: settingsTitle.bottom
        anchors.bottom: saveButton.top
        anchors.leftMargin: 50
        anchors.rightMargin: 0
        anchors.bottomMargin: 50
        clip: true

        Column {
            spacing: 20

            SettingsEntry {
                entryName: "Database path"
                TextField {
                    text: "~/.texviper"
                    width: 300
                }
            }
            SettingsEntry {
                entryName: "Database name"
                TextField {
                    text: "texviper.db"
                    width: 300
                }
            }
            SettingsEntry {
                entryName: "Accent color"
                TextField {
                    text: "#432432"
                    width: 300
                }
            }
            SettingsEntry {
                entryName: "Editor font"
                TextField {
                    text: "Source Code Pro"
                    width: 300
                }
            }
        }
    }

    Text {
        anchors.verticalCenter: parent.verticalCenter
        x: 25
        y: 25
        color: "#979797"
        text: "Settings"
        font.pixelSize: 16
    }

    Button {
        id: saveButton
        text: "Save"
        y: window.height - 100
        x: 50
        width: 250
    }
}
