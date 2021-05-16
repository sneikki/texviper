from views.view import View
from config.config import config


class RootView(View):
    def __init__(self, engine):
        super().__init__(engine)

        accent = config.get_value('accent_color')
        self.root.set_accent(accent)
