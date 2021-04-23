from PySide2.QtCore import QObject, Slot

class HomeView(QObject):
    def __init__(self):
        super().__init__()

    @Slot()
    def click(self):
        print("click")
