import QtQuick 2.12
import QtQuick.Controls 2.12

TabButton {
    property var project_id

    width: implicitWidth

    onClicked: {
        project_view.show_project(project_id)
    }
}