from kivy.uix.screenmanager import Screen


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)

    def before_load(self, ): self.update_toolbar()

    def update_toolbar(self):
        pass
