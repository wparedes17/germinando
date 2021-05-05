from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.event import EventDispatcher

import time
import threading
import os

with open("SplitScreen.kv", encoding='utf8') as f:
            Builder.load_string(f.read())

class HomeScreen(BoxLayout):
    
    def build(self):
        sm = ScreenManager(transition=NoTransition())
        sm_main = ScreenManager(transition=NoTransition())
        return sm, sm_main
            

class Panel(Screen):
    
    user_name = StringProperty("")
    image_path = StringProperty("")
    
    def __init__(self, **kwargs):
        archivo = open("user_info.txt","r+")
        self.user_name = archivo.readline().strip()
        self.image_path = archivo.readline().strip()
        archivo.close()
        super(Panel, self).__init__(**kwargs)
    
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
    
    def __init__(self, **kwargs):
        super(Panel2, self).__init__(**kwargs)
    
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


class Screen1(Screen, EventDispatcher):
    
    loadfile = ObjectProperty(None)
    text_input = ObjectProperty(None)
    user_name_new = StringProperty("Escribe tu nombre")
    contador = NumericProperty(0)
    panel = StringProperty("")
    image_path_new = StringProperty("No_image")
    load_success = StringProperty("Ninguna imagen se ha cargado")
    label_color = ListProperty([1,0,0,1])

   
    def __init__(self, **kwargs):
        super(Screen1, self).__init__(**kwargs)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        try:
            self.image_path_new = str(filename[0])
            self.load_success = "Imagen cargada exitosamete"
            self.label_color = [0,1,0,1]
        except:
            pass
        self.dismiss_popup()
    
    def apply_changes(self):
        
        archivo = open("user_info.txt","r+")
        self.user_name_old = archivo.readline().strip()
        self.image_path_old = archivo.readline().strip()
        archivo.close()
        
        archivo = open("user_info.txt","w")
        self.user_name = self.text_input.text
        if self.user_name_new != "Escribe tu nombre":
            archivo.write(self.user_name_new+"\n")
        else:
            archivo.write(self.user_name_old+"\n")
        if self.image_path_new != "No_image":
            archivo.write(self.image_path_new)
        else:
            archivo.write(self.image_path_old)
        archivo.close()
        
        if self.contador == 0:
            self.contador += 1
            self.panel = "panel2"
        else:
            self.contador = 0
            self.panel = "panel_main"        
        

class Screen2(Screen):
    def __init__(self, **kwargs):
        super(Screen2, self).__init__(**kwargs)

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
