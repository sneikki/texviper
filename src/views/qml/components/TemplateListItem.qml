import QtQuick 2.12
import QtQuick.Controls 2.12

Row {
    property var template_id
    property var name
    spacing: 10

    Text {
        id: templateName
        
        width: 200
        text: name || ""
        anchors.verticalCenter: parent ? parent.verticalCenter : undefined
    }

    Button {
        text: "Edit"
        onClicked: template_view.edit_clicked(template_id)
    }

    Button {
        text: "Remove"
        onClicked: {
            template_view.remove_template(template_id)
        }
    }
}
