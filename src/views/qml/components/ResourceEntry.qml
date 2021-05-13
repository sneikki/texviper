import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    property var name
    property var resource_id
    width: parent ? parent.width : 0
    height: 25
    color: ma.hover ? '#eee' : '#fff'
    
    Text {
        anchors.fill: parent
        verticalAlignment: Text.AlignVCenter
        anchors.leftMargin: 10
        elide: Text.ElideRight
        text: name
    }

    MouseArea {
        id: ma
        property var hover: false
        anchors.fill: parent
        hoverEnabled: true
        onEntered: hover = true
        onExited: hover = false
        acceptedButtons: Qt.LeftButton | Qt.RightButton

        onDoubleClicked: project_view.open_resource(name, resource_id)
        onClicked: {
            if (mouse.button === Qt.RightButton) {
                resourceMenu.popup()
            }
        }
    }

    Menu {
        id: resourceMenu

        MenuItem {
            text: 'Remove'
            onTriggered: {
                project_view.remove_resource(resource_id)
            }
        }
    }
}