import QtQuick 2.12
import QtQuick.Controls 2.12

Row {
    property var entryName
    spacing: 20

    Text {
        text: entryName
        width: 250
        anchors.verticalCenter: parent.verticalCenter
    }
}
