from PySide2.QtCore import QObject, Slot

class ProjectView(QObject):
    def __init__(self):
        super().__init__()
    
    @Slot()
    def click(self):
        print("project click")
