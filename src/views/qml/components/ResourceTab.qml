import QtQuick 2.12
import QtQuick.Controls 2.12

TabButton {
    id: tab_button
    property var resource_id

    width: implicitWidth + 30

    Image {
        source: 'close_icon.svg'
        width: 10
        height: 10
        anchors.right: tab_button.right
        anchors.rightMargin: 10
        anchors.top: tab_button.top
        anchors.topMargin: 10

        MouseArea {
            anchors.fill: parent

            onClicked: {
                tab_button.destroy()
                project_view.close_resource(resource_id)
            }
        }
    }

    onClicked: {
        project_view.show_resource(resource_id)
    }
}
