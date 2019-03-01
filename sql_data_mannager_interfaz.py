import kivy
kivy.require('1.0.5')

from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty

class Controller(BoxLayout):

    screen_main = ObjectProperty()

    def screen_bd(self):
        self.remove_widget(self.screen_main)

class ControllerApp(App):

    def build(self):
        return Controller()


if __name__ == '__main__':
    ControllerApp().run()
