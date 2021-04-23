import QtQuick 2.12
import QtQuick.Controls 2.12

Rectangle {
    property var name
    property var modified
    width: 200
    height: 250
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
            y: 130
            width: parent.width
            height: 65
            color: "#eeeeee"
        }

        Text {
            x: 31
            y: 88
            color: "#999999"
            text: qsTr("Preview N/A")
            anchors.left: parent.left
            anchors.top: parent.top
            font.pixelSize: 16
            anchors.leftMargin: 56
            anchors.topMargin: 88
        }
    }

    Text {
        x: 8
        y: 205
        width: 184
        height: 15
        text: name
        elide: Text.ElideRight
        font.pixelSize: 12
    }

    Text {
        x: 8
        y: 224
        width: 184
        height: 15
        color: "#a2a2a2"
        text: modified
        elide: Text.ElideRight
        font.pixelSize: 12
    }
}