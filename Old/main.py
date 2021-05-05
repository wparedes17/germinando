from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout


with open("Software.kv", encoding='utf8') as f:
            Builder.load_string(f.read())


class Login(Screen):

    def check_password(self):
        self.password = '11235'
        if self.ids.passw.text == str(self.password):
            self.parent.current = 'settings'

class SettingsScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(Login(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))


class MyApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()
