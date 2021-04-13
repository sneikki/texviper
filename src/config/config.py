from json import dumps


class Config:  # pylint: disable=too-few-public-methods
    def create_project_config(self, project):
        project_config = dict()

        project_config['name'] = project.name
        project_config['id'] = project.project_id

        return dumps(project_config)

config = Config()
