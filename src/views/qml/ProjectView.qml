import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11
import 'components'

Item {
    property var projectCount
    objectName: 'projectView'
    width: parent.width
    height: parent.height


    Item {
        width: parent.width
        height: parent.height

        MenuBar {
            id: menubar
            Menu {
                title: 'File'
                Action {
                    text: 'Add resource'
                    shortcut: StandardKey.New
                    onTriggered: project_view.add_resource()
                }
                MenuSeparator { }
                Action { 
                    text: 'Save resource'
                    shortcut: StandardKey.Save
                    onTriggered: project_view.save_resource()
                }
                Action {
                    text: 'Save project'
                    onTriggered: project_view.save_project()
                }
                MenuSeparator { }
                Action {
                    text: 'Close project'
                    onTriggered: project_view.close_project()    
                }
            }

            Menu {
                title: 'Project'
                Action { text: 'Build' }
                Action { text: 'Export' }
            }
        }

        TabBar {
            id: projectsTab
            objectName: 'projectsTab'
            width: parent.width
            contentHeight: 30
            anchors.top: menubar.bottom

            function remove(project_id) {
                for (var i = 0; i < projectsTab.children.length; i++) {    
                    console.log(projectsTab.children[i].project_id)
                }
            }
        }

        StackLayout {
            id: projectStack
            objectName: 'projectStack'
            
            anchors.top: projectsTab.bottom
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.margins: 0

            function add_editor_view(name, project_id) {
                var component = Qt.createComponent('EditorView.qml')
                var item = component.createObject(null, { projectName: name, project_id: project_id })
                projectStack.children.push(item)
            }

            function find_editor(project_id) {
                for (var i = 0; i < projectStack.children.length; i++) {
                    if (projectStack.children[i].project_id == project_id) {                
                        return projectStack.children[i]
                    }
                }
            }

            function show_project(project_id) {
                for (var i = 0; i < projectStack.children.length; i++) {
                    if (projectStack.children[i].project_id == project_id) {                
                        projectStack.currentIndex = i
                        break
                    }
                }
            }
        }
    }

    // Component {
    //     id: emptyProjectView

    //     Text {
    //         horizontalAlignment: Text.AlignHCenter
    //         verticalAlignment: Text.AlignVCenter
    //         width: parent.width
    //         height: parent.height
    //         text: 'No projects open'
    //         font.pixelSize: 32
    //         color: '#a2a2a2'
    //         font.bold: true
    //     }
    // }
}
