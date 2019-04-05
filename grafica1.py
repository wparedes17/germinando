from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import runTouchApp
import seaborn as sns
import openpyxl
import pandas as pd
import matplotlib
import numpy as np
import matplotlib.pyplot as plt



class Caja(BoxLayout):
	def __init__(self, **kwargs):
		super(Caja,self).__init__(**kwargs)

    
		mercados=[]
		with open('Mercados.txt') as lineas:
			for linea in lineas:
				mercados.append(linea)
		
				
		spinner = Spinner(text='Mercado a analizar',values=mercados,
									size_hint_x= 0.7,size_hint_y= None,height=65,
									background_color= ( 0, .5, .08, 1),background_normal="down2.png",
									color=(0,0,0,.5))
		
		def myFunction(spinner,text):
			print (text)
		spinner.bind(text=myFunction)	
		self.ids.Mercados.add_widget(spinner)
		
		
		spinner = Spinner(text='Periodo a analizar',values=("Completo", "Ultimo año", "Ultimos 2 años", "Ultimos 3 años", "Ultimos 4 años"),
									size_hint_x= 0.2,size_hint_y= None,height=65,
									background_color= ( 0, 1, 0.9333, 1),background_normal="down2.png",
									color=(0,0,0,.5))
		
		def myFunction(spinner,text):
			print (text)
		spinner.bind(text=myFunction)
		self.ids.Mercados.add_widget(spinner)
					
		
		mybutton = Button(text= "Visualizar",size_hint_x= 0.1,
					size_hint_y=None, background_color=( .9372, .4980, 0.1019, 1),background_normal="down1.png",
					height=65)
		self.ids.Mercados.add_widget(mybutton)
		mybutton.bind(on_press=self.visualizar)			
		
							
	def visualizar(self,event):
		sns.set(style="whitegrid")
		doc = pd.read_csv("Aguascalientes Centro Comercial Agropecuario de Aguascalientes_Chiles Secos.csv")
		sns_plot= sns.lineplot(x="FECHA", y="PRECIO_PROMEDIO",data=doc)
		fig = sns_plot.get_figure()
		fig.savefig("image1.png",transparent=True)
		picture = Image(source = 'image1.png')
		self.ids.Grafica.add_widget(picture)
         
		
		
		
		
		
		
class Grafica1App(App):
	def build(self):
		return Caja()
		
			
if __name__ == '__main__':
    Grafica1App().run()
