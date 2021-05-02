import shutil


class FileSystem:
    def directory_exists(self, path):
        return path.exists()

    def file_exists(self, path):
        return path.exists()

    def directory_empty(self, path):
        return next(path.iterdir(), None) is None

    def create_directory(self, path):
        path.mkdir(parents=True, exist_ok=True)

    def copy(self, source, destination):
        shutil.copy(source, destination)

    def create_file(self, path):
        path.touch()

    def write(self, path, text):
        path.write_text(text)

    def remove_directory(self, path):
        shutil.rmtree(path)

    def remove_file(self, path):
        path.unlink()


file_system = FileSystem()
