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

with open("SplitScreen.kv", encoding='utf8') as f:
            Builder.load_string(f.read())

class HomeScreen(BoxLayout):
    
    user_name = StringProperty("Perenganito")
            

class Panel(Screen):
    
    user_name = StringProperty("")
    image_path = StringProperty("")
    
    def on_enter(self, *args):
        thread = threading.Thread(target=self.load_user)
        thread.daemon = True
        thread.start()

    def load_user(self, *args):
        archivo = open("user_info.txt","r+")
        self.user_name = archivo.readline().strip()
        self.image_path = archivo.readline().strip()
        archivo.close()
        
class Panel2(Screen):
    
    user_name = StringProperty("")
    image_path = StringProperty("non-user.jpg")
    
    def on_enter(self, *args):
        thread = threading.Thread(target=self.load_user)
        thread.daemon = True
        thread.start()

    def load_user(self, *args):
        archivo = open("user_info.txt","r+")
        self.user_name = archivo.readline().strip()
        self.image_path = archivo.readline().strip()
        archivo.close()
        
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Screen1(Screen):
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    user_name = StringProperty("Escribe tu nombre")
    contador = NumericProperty(0)
    panel = StringProperty("")
   

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        if self.contador == 0:
            self.contador += 1
            self.panel = "panel2"
        else:
            self.contador = 0
            self.panel = "panel_main"        
        archivo = open("user_info.txt","w")
        self.user_name = self.text_input.text
        archivo.write(self.user_name+"\n")
        try:
            archivo.write(str(filename[0]))
        except:
            pass
        archivo.close()
        self.dismiss_popup()

class Screen2(Screen):
    pass

class Principal(App):
    def build(self):
        return HomeScreen()


Factory.register('Principal', cls=Principal)
Factory.register('Panel', cls=Panel)
Factory.register('HomeScreen', cls=HomeScreen)
Factory.register('Screen2', cls=Screen2)
Factory.register('Screen1', cls=Screen1)
Factory.register('LoadDialog', cls=LoadDialog)

if __name__ == "__main__":
    Principal().run()
