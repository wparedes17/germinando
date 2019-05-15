from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.checkbox import CheckBox
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout


with open("Software.kv", encoding='utf8') as f:
            Builder.load_string(f.read())


class Test(Screen):
    password= "11235"
    def clave(self):
        contraseña=input()
        if contraseña==password:
            print(contraseña)
        else:
            print("error en clave")
    def login(self, instance):
        print(self.password.text)
        if self.password.text == 'password':
            popup = Popup(title='Logged',content=Label(text='Logged in successfully, admin'))
            popup.open()
        else:
            popup = Popup(title='Wrong password',content=Label(text='Wrong password, admin. Go away.'))
            popup.open()


class SettingsScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(Test(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))


class MyApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()