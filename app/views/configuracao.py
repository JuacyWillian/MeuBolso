from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

kv = """
<Configuracao>:
    on_pre_enter: self.before_load()
    MDLabel:
        text: 'Config'
"""

Builder.load_string(kv)


class Configuracao(Screen):
    def __init__(self, **kwargs):
        super(Configuracao, self).__init__(**kwargs)

    def before_load(self, ): self.update_toolbar()

    def update_toolbar(self):
        pass
