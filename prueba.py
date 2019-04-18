import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout

class Box01(BoxLayout):
    def build(self):
      return Botonrd()
    
class Botonrd(BoxLayout):
    def build(self):
        btn=Button(text="Cargar base de datos")
        btd=Button(text="Analisis descriptivo")
        btp=Button(text="Analisis predictivo y toma de decisiones")

        layout=BoxLayout()
        layout.orientation="vertical"
        layout.add_widget(btn)
        layout.add_widget(btd)
        layout.add_widget(btp)

class TestApp(App): #el npmbre de la clase app debe ser igual al .kv
    def build(self):
        return Box01()
   

if __name__ == '__main__':
    TestApp().run()