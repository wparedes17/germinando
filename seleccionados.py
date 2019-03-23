import kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.label import Label
from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp
from kivy.graphics import Color, Rectangle



class Etiqueta(BoxLayout):
	def __init__(self, **kwargs):
		super(Etiqueta,self).__init__(**kwargs)
		self.cols=2
		Window.clearcolor = (1, 1, 1, 1)
		layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
		layout.bind(minimum_height=layout.setter('height'))
		mercados=open("Nombres.txt","r")
		registro=[]
		with open('Registros.txt') as lineas:
			for linea in lineas:
				registro.append(linea)
		contador=0
		border=(10,10,10,10),background_color=( 1, 0, 0, 1),background_normal="normal.png",
		for i in mercados:
			layout.add_widget(Label(markup =True,text="Mercado de " + i,
				id=str(i),size_hint_x= 0.8,size_hint_y=None,color=(1, .3, .1, 1), 
				size_font = self.width*0.4,height=50))
	
			if  'Actualizado' in str(registro[contador]):	
				layout.add_widget(Button(id=str(i),size_hint_x= 0.1,
					size_hint_y=None, size_font = self.width*0.4,background_normal="verde.png",
					color=(0, 0, 0, 1),height=50,background_down= 'amarillo.png'))
				contador=contador+1
			elif 'Desactualizado' in str(registro[contador]):
				layout.add_widget(Button(id=str(i),size_hint_x= 0.1,
					size_hint_y=None, size_font = self.width*0.4,background_normal="rojo.png",
					color=(0, 0, 0, 1),height=50,background_down= 'amarillo.png'))
				contador=contador+1
			elif 'Semidesactualizado' in str(registro[contador]):
				layout.add_widget(Button(id=str(i),size_hint_x= 0.1,
					size_hint_y=None, size_font = self.width*0.4,background_normal="amarillo.png.png",
					color=(0, 0, 0, 1),height=50,background_down= 'amarillo.png'))
				contador=contador+1
												
		root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
		root.add_widget(layout)

		runTouchApp(root)

class SeleccionadosApp(App):
	def build(self):
		return Etiqueta()
		
			
if __name__ == '__main__':
    SeleccionadosApp().run()			
		
