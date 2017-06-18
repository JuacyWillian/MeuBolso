from kivy.app import App
from kivy.uix.screenmanager import Screen


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

    def before_load(self, ):
        self.update_toolbar()

    def update_toolbar(self, ):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []
