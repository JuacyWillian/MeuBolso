from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

kv = """
<Home>:
    nome: 'home'
    on_pre_enter: self.before_load()

    MDLabel:
        markup: True
        text: '%s Hello Home Screen'%icon('mdi-home')
"""
Builder.load_string(kv)


class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)

    def before_load(self, ):
        self.update_toolbar()

    def update_toolbar(self, ):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []
