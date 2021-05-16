import shutil


class FileSystem:
    def directory_exists(self, path):
        """ Checks if a given path exists.

            Args:
                path (string): Path to check
        """
        return path.exists()

    def file_exists(self, file_name):
        """ Checks if a given file exists.

            Args:
                file_name (string): File to check
        """
        return file_name.exists()

    def directory_empty(self, path):
        """ Checks if a given directory is empty

            Args:
                path (string): Path of the directory to check
        """
        return next(path.iterdir(), None) is None

    def create_directory(self, path):
        """ Creates a directory in a given path. Parent
            directiories are created, if missing.

            Args:
                path (string): Path of the directory to create
        """
        path.mkdir(parents=True, exist_ok=True)

    def copy(self, source, destination):
        """ Copies a file from source path
            to destination path.

            Args:
                source (string): Path of the source file
                destination (string): Path of the destination file
        """
        shutil.copy(source, destination)

    def create_file(self, path):
        """ Creates a file in a given path.

            Args:
                path (string): Path of the file to create
        """
        path.touch()

    def write(self, path, text):
        """ Writes text to a file.

            Args:
                path (string): Path of the file to write to
                text (string): Text to write to the file
        """
        path.write_text(text)

    def remove_directory(self, path):
        """ Removes a directory

            Args:
                path (string): Path of the directory ro remove
        """
        shutil.rmtree(path)

    def remove_file(self, path):
        """ Removes a file

            Args:
                path (string): Path of the file to remove
        """
        path.unlink()


file_system = FileSystem()
