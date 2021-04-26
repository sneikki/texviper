import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    property var project_id
    property var name
    property var modified
    width: 200
    height: 260
    color: "white"
    radius: 8
    border.color: "#eeeeee"

    Rectangle {
        x: 0
        y: 0
        width: parent.width
        height: 200
        color: "#eeeeee"
        radius: 8

        Rectangle {
            x: 0
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            width: parent.width
            height: 65
            color: "#eeeeee"
        }
    }

    Text {
        x: 16
        y: 210
        width: 184
        height: 15
        text: name
        elide: Text.ElideRight
        font.pixelSize: 12
    }

    Text {
        x: 16
        y: 234
        width: 184
        height: 15
        color: "#a2a2a2"
        text: modified
        elide: Text.ElideRight
        font.pixelSize: 12
    }
}