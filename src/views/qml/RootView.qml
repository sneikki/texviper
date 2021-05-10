import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.11
import QtQuick.Controls.Material 2.12
import QtQuick.Dialogs 1.1

ApplicationWindow {
    id: window
    width: 960
    height: 640
    minimumWidth: 640
    minimumHeight: 540
    visible: true
    color: 'white'
    title: qsTr('Texviper')

    function set_accent(accent) {
        Material.accent = accent
    }

    TabBar {
            id: menu
            width: parent.width

            TabButton {
                text: 'Home'

                onClicked: {
                    windowsLayout.currentIndex = 0
                }
            }

            TabButton {
                text: 'Projects'
            
                onClicked: {
                    windowsLayout.currentIndex = 1
                }
            }

            TabButton {
                text: 'Settings'
            
                onClicked: {
                    windowsLayout.currentIndex = 2
                }
            }

            TabButton {
                text: 'Templates'
            
                onClicked: {
                    windowsLayout.currentIndex = 3
                }
            }
        }

    StackLayout {
        id: windowsLayout
        objectName: 'windowsLayout'
        anchors.top: menu.bottom
        anchors.topMargin: 0
        width: parent.width
        height: parent.height

        currentIndex: 0

        HomeView {

        }

        ProjectView {

        }

        SettingsView {

        }

        TemplateView {
            
        }

        function set_current(current) {
            currentIndex = current
            menu.currentIndex = current
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
