from PySide2.QtCore import QThread


class BuildThread(QThread):
    def __init__(self, target, callback=None):
        super().__init__()
        self.target = target
        if callback:
            self.finished.connect(lambda: callback(self.state))

    def run(self, *args, **kwargs):
        self.state = self.target(*args, **kwargs)
        
