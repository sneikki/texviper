import shutil

class FileSystem:
    def directory_exists(self, path):
        return path.exists()

    def directory_empty(self, path):
        return next(path.iterdir(), None) is None

    def create_directory(self, path):
        path.mkdir(parents=True,exist_ok=True)

    def copy(self, source, destination):
        shutil.copy(source, destination)

    def create_file(self, path):
        path.touch()

    def write(self, path, text):
        path.write_text(text)

file_system = FileSystem()
