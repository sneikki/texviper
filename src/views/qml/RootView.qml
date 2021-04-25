import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.11

ApplicationWindow {
    property var active: 0
    id: window
    width: 960
    height: 640
    minimumWidth: 640
    minimumHeight: 540
    visible: true
    color: "white"

    title: qsTr("hello world")

    Rectangle {
        id: menu
        height: 30
        width: parent.width
        color: "#dfdfdf"
        
        Row {
            id: row
            x: 0
            y: 0
            width: 200
            height: 400
            layoutDirection: Qt.LeftToRight
            rotation: 0

            Rectangle {
                id: home_btn
                width: window.width / 4
                height: 30
                color: (window.active === 0) ? "#189648" : "#d2d2d2"

                Text {
                    id: text1
                    y: 5
                    color: (window.active === 0) ? "#ffffff" : "#5b5b5b"
                    text: qsTr("Home")
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 16
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.capitalization: Font.AllUppercase
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        windowsLayout.currentIndex = 0
                        window.active = 0
                    }
                }
            }

            Rectangle {
                id: project_btn
                width: window.width / 4
                height: 30
                color: (window.active === 1) ? "#189648" : "#d2d2d2"

                Text {
                    id: text2
                    anchors.horizontalCenter: parent.horizontalCenter
                    y: 5
                    color: (window.active === 1) ? "#ffffff" : "#5b5b5b"
                    text: "Projects"
                    font.pixelSize: 16
                    font.capitalization: Font.AllUppercase
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        windowsLayout.currentIndex = 1
                        window.active = 1
                    }
                }
            }

            Rectangle {
                id: settings_btn
                width: window.width / 4
                height: 30
                color: (window.active === 2) ? "#189648" : "#d2d2d2"

                Text {
                    id: text3
                    anchors.horizontalCenter: parent.horizontalCenter
                    y: 5
                    color: (window.active === 2) ? "#ffffff" : "#5b5b5b"
                    text: qsTr("Settings")
                    font.pixelSize: 16
                    font.capitalization: Font.AllUppercase
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        windowsLayout.currentIndex = 2
                        window.active = 2
                    }
                }
            }

            Rectangle {
                id: template_btn
                width: window.width / 4
                height: 30
                color: (window.active === 3) ? "#189648" : "#d2d2d2"

                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    y: 5
                    color: (window.active === 3) ? "#ffffff" : "#5b5b5b"
                    text: qsTr("Templates")
                    font.pixelSize: 16
                    font.capitalization: Font.AllUppercase
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        windowsLayout.currentIndex = 3
                        window.active = 3
                    }
                }
            }
        }

    }

    StackLayout {
        id: windowsLayout
        anchors.top: menu.bottom
        anchors.topMargin: 0
        width: parent.width

        currentIndex: 0

        HomeView {

        }

        ProjectView {

        }

        SettingsView {

        }

        TemplateView {
            
        }
    }
}
