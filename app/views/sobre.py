from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from app.lang import s as strings

kv = """
<Sobre>:
    on_pre_enter: self.before_load()
    ScrollView:
        do_scroll_x: False

        BoxLayout:
            orientation: 'vertical'
            padding: '10dp'
            spacing: '10dp'

            AsyncImage:
                size_hint_y: None
                height: '150dp'
                allow_stretch: True
                source: 'logo.jpg'

            MDLabel:
                font_style: 'Body2'
                text: root.about_text
                valign: 'top'
                size: self.texture_size
"""
Builder.load_string(kv)


class Sobre(Screen):
    about_text = StringProperty()

    def __init__(self, **kwargs):
        super(Sobre, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.about_text = strings.app_description

    def before_load(self, ):
        self.update_toolbar()

    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []
