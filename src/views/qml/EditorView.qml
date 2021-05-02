import QtQuick 2.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import QtQuick.Controls.Styles 1.4
import 'components'

SplitView {
    property var projectName
    property var project_id
    property var editorId

    function add_resource(name, resource_id) {
        var component = Qt.createComponent('components/ResourceEntry.qml')
        var item = component.createObject(null, { name, resource_id })
        resourceList.children.push(item)
    }

    function open_resource(name, source, resource_id) {
        var component = Qt.createComponent('components/EditPanel.qml')
        var item = component.createObject(null, { source, resource_id })
        resourcePanel.children.push(item)

        var component = Qt.createComponent('components/ResourceTab.qml')
        var item = component.createObject(null, { resource_id, text: name })
        resourceTabBar.addItem(item)
    }

    function show_resource(resource_id) {
        for (var i = 0; i < resourcePanel.children.length; i++) {
            
            if (resourcePanel.children[i].resource_id == resource_id) {       
                resourcePanel.currentIndex = i
                break
            }
        }
    }

    function close_resource(resource_id) {
        for (var i = 0; i < resourcePanel.children.length; i++) {
            
            if (resourcePanel.children[i].resource_id == resource_id) {       
                resourcePanel.children[i].destroy()
                break
            }
        }
    }

    Item {
        id: resources

        SplitView.minimumWidth: 250
        SplitView.preferredWidth: 300
        SplitView.maximumWidth: 350
        height: parent.height

        Item {
            anchors.fill: parent
            anchors.margins: 25

            Text {
                id: projectNameLabel
                text: projectName
                font.bold: true
                font.pixelSize: 14
                color: '#333'
                width: parent.width
                height: 30
            }

            ScrollView {
                anchors.top: projectNameLabel.bottom
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.margins: 0

                Column {
                    id: resourceList

                    width: parent.width
                    height: parent.height
                    spacing: 10

                    
                }
            }
        }
    }

    Item {
        id: editor

        SplitView.minimumWidth: 300
        SplitView.preferredWidth: (parent.width - 200) / 2

        TabBar {
            id: resourceTabBar
            width: parent.width
            contentHeight: 30
            
        }

        StackLayout {
            id: resourcePanel
            anchors.top: resourceTabBar.bottom
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.left: parent.left    
        }
    }

    Item {
        id: preview

        SplitView.minimumWidth: 300
        SplitView.preferredWidth: (parent.width - 200) / 2
    }

    handle: Rectangle {
        implicitWidth: 4
        color: SplitHandle.pressed ? '#eee' : '#ddd'
    }

}