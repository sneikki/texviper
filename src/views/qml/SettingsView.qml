import QtQuick 2.12
import QtQuick.Controls 2.12
import 'components'

Item {
    width: parent.width
    height: parent.height

    ScrollView {
        anchors.fill: parent

        Text {
            id: settingsTitle
            text: 'Settings'
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 50
            anchors.topMargin: 50
            font.pixelSize: 20
            color: '#999999'
        }

        Column {
            id: settingsList
            anchors.top: settingsTitle.bottom
            anchors.left: parent.left
            anchors.topMargin: 50
            anchors.leftMargin: 50
            width: parent.width
            spacing: 20

            SettingsEntry {
                entryName: 'Database path'

                TextField {
                    objectName: 'dbPath'
                    width: 200
                }
            }

            SettingsEntry {
                entryName: 'Database name'

                TextField {
                    objectName: 'dbName'
                    width: 200
                }
            }

            SettingsEntry {
                entryName: 'Default project location'

                TextField {
                    objectName: 'projectLocation'
                    width: 200
                }
            }

            SettingsEntry {
                entryName: 'Default template location'

                TextField {
                    objectName: 'templateLocation'
                    width: 200
                }
            }

            SettingsEntry {
                entryName: 'Root filename'

                TextField {
                    objectName: 'rootFilename'
                    width: 200
                }
            }

            SettingsEntry {
                entryName: 'Accent color'

                TextField {
                    objectName: 'accentColor'
                    width: 200
                }
            }

            SettingsEntry {
                entryName: 'Editor font'

                TextField {
                    objectName: 'editorFont'
                    width: 200
                }
            }
        }

        Button {
            id: saveSettingsButton
            text: 'Save'
            anchors.top: settingsList.bottom
            anchors.left: parent.left
            anchors.topMargin: 50
            anchors.leftMargin: 50
            width: 200
            onClicked: settings_view.save_settings()
        }
    }
}
