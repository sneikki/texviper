class DirectoryNotEmptyError(Exception):
    pass


class DatabaseConnectionError(Exception):
    pass


class ProjectExistsError(Exception):
    pass


class InvalidValueError(Exception):
    pass


class BuildError(Exception):
    pass
