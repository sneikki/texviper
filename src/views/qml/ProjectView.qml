import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import QtQuick.Controls.Styles 1.4
import QtQuick.Controls 1.4 as C1
import 'components'

Item {
    id: projectView
    objectName: 'projectView'
    width: parent.width
    height: parent.height
    property var openProject

    Loader {
        sourceComponent: openProject ? openView : emptyView
        anchors.fill: parent
    }

    Component {
        id: emptyView

        Text {
            text: 'No project opened'
            font.pixelSize: 32
            font.bold: true
            color: '#a2a2a2'
            width: parent.width
            height: parent.height
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }

    Component {
        id: openView
        
        C1.SplitView {
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.margins: 0

            Item {
                id: resources
                width: 300
                Layout.minimumWidth: 300
                Layout.maximumWidth: 400
                height: parent.height
                
                Item {
                    id: container
                    anchors.fill: parent
                    anchors.margins: 25
                    
                    Text {
                        id: projectName
                        text: 'Johdatus lineaarialgebraan'
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        font.bold: true
                        color: '#333'
                    }
                    
                    ScrollView {
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: projectName.bottom
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 0
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0
                        anchors.topMargin: 25
                        
                        Column {
                            id: resourceList
                            objectName: 'resourceList'
                            
                            anchors.fill: parent
                        }
                    }
                }
            }

            Item {
                id: editor
                Layout.minimumWidth: 300
                width: parent.width / 2 - 150
                height: parent.height



            }

            Item {
                id: preview
                Layout.minimumWidth: 300
                width: parent.width / 2 - 150
                height: parent.height

            }
        }
    }
}
