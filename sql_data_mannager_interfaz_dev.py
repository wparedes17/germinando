import kivy
kivy.require('1.0.5')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.image import Image
from kivy.uix.label import Label

import time
import threading

class ScreenOne(Screen):
    health_points = NumericProperty(0)

    def on_health_points(self, instance, value):
        if value > 99:
            self.changeScreen()

    def on_enter(self, *args):
        thread = threading.Thread(target=self.bleed)
        thread.daemon = True
        thread.start()

    def bleed(self, *args):
        while self.health_points < 100:
            self.health_points += 5
            time.sleep(0.1)

    def displayScreenThenLeave(self):
        self.changeScreen()

    def changeScreen(self):
        if self.manager.current == 'screen2':
            self.manager.current = 'screen1'
        else:
            self.manager.current = 'screen2'


class ScreenTwo(Screen):
    pass

class ScreenThree(Screen):
    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)


class ScreenFour(Screen):

    def __init__(self, **kwargs):
        super(ScreenFour, self).__init__(**kwargs)

    num_lines = NumericProperty(-1)

    def on_enter(self, *args):
        thread = threading.Thread(target=self.read_repository)
        thread.daemon = True
        thread.start()

    def read_repository(self):
        registro = open("repositorio.txt","w+")
        registro.close()
        self.num_lines = 1
        if self.num_lines > 0:
            etiqueta = Label(text="Total de fuentes encontradas: "+str(self.num_lines-1))
            self.add_widget(etiqueta)


class Manager(ScreenManager):

    screen_one = ObjectProperty(None)
    screen_two = ObjectProperty(None)
    screen_three = ObjectProperty(None)
    screen_four = ObjectProperty(None)

class ScreensApp(App):

    def build(self):
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    ScreensApp().run()
