import QtQuick 2.12
import QtQuick.Controls 2.12

ScrollView {
    property var source
    property var resource_id
    id: scrollView
    clip: true
    height: parent ? parent.height : 0
    width: parent.width

    function get_source() {
        return editTemplateDialogContent.text
    }

    TextEdit {
        objectName: 'editTemplateDialogContent'
        id: editTemplateDialogContent
        color: '#666666'
        text: source
        anchors.fill: parent
        font.pixelSize: 12
        wrapMode: Text.WrapAnywhere
        selectionColor: '#9b9b9b'
        font.family: project_view.get_font()
        padding: 25
        selectByMouse: true
    }
}