from PySide2.QtCore import QObject, Slot

class SettingsView(QObject):
    def __init__(self):
        super().__init__()
    
    @Slot()
    def click(self):
        print("settings click")
