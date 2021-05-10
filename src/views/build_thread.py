from PySide2.QtCore import QThread


class BuildThread(QThread):
    def __init__(self, target, callback=None):
        super().__init__()
        self.target = target
        if callback:
            self.finished.connect(callback)

    def run(self, *args, **kwargs):
        self.target(*args, **kwargs)
