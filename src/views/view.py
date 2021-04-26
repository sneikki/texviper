from PySide2.QtCore import QObject

class View(QObject):
    def __init__(self, engine):
        super().__init__()
        
        self.engine = engine
        self.root = self.engine.rootObjects()[0]
