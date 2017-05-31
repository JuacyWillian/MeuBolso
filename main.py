from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.theming import ThemeManager


class HomeScreen(Screen):
    def update_toolbar(self, ):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []


class ContactScreen(Screen):
    def update_toolbar(self, ):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['account-plus',
             lambda x: app.root.ids.scr_mngr.switch_to(NewContactScreen())]
        ]


class NewContactScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['account-check', lambda x: self.save_contact()],
            ['account-off',
             lambda x: app.root.ids.scr_mngr.switch_to(ContactScreen())]
        ]

    def save_contact(self):
        pass


class IncomeScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['plus-circle',
             lambda x: app.root.ids.scr_mngr.switch_to(NewIncomeScreen())]
        ]


class NewIncomeScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['content-save', lambda x: self.save_income()],
            ['close',
             lambda x: app.root.ids.scr_mngr.switch_to(IncomeScreen())]
        ]

    def save_income(self):
        pass


class EditIncomeScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = [
            ['content-save', lambda x: self.save_income()],
            ['close',
             lambda x: app.root.ids.scr_mngr.switch_to(IncomeScreen())]
        ]

    def save_income(self):
        pass


class SettingsScreen(Screen):
    def update_toolbar(self):
        pass


class AboutScreen(Screen):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []


class MyScreenManager(ScreenManager):
    def update_toolbar(self):
        app = App.get_running_app()
        toolbar = app.root.ids['toolbar']
        toolbar.right_action_items = []

    def change_screen(self, screen_name):
        self.current = screen_name


class MeuBolsoApp(App):
    theme_cls = ThemeManager()


if __name__ == '__main__':
    app = MeuBolsoApp()
    app.run()
