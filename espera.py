import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


import time
import threading
import os
	
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
        

class Manager(ScreenManager):

    screen_one = ObjectProperty(None)




class EsperaApp(App):

    def build(self):
        m = Manager(transition=NoTransition())
        return m

if __name__ == "__main__":
    EsperaApp().run()

