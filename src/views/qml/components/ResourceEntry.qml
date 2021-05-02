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

        text: name
    }

    MouseArea {
        id: ma
        property var hover: false
        anchors.fill: parent
        hoverEnabled: true
        onEntered: hover = true
        onExited: hover = false

        onDoubleClicked: project_view.open_resource(name, resource_id)
    }
}