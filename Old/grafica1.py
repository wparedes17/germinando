
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
import csv
import os
from datetime import datetime
from pandas import read_csv


class Caja(BoxLayout):
	def __init__(self, **kwargs):
		super(Caja,self).__init__(**kwargs)

		
		mercados=[]
		with open('Selecciones.txt',encoding="utf-8") as lineas:
			for linea in lineas:
				mercados.append(linea)
		
				
		spinner = Spinner(markup = True,text='[color=F8F8FF]Mercado a analizar[/color]',values=mercados,
									size_hint_x=1,size_hint_y= None,height=65,
									background_color= ( 0.5, .5, 0, 1),background_normal="down2.png",
									color=(0,0,0,.5))
		
		def functionOne(spinner,text):
			global mercado_elegido
			mercado_elegido=text 
			mercado_elegido=mercado_elegido.rstrip('\n')
			mercado_elegido=mercado_elegido.rstrip(' ')
			print(mercado_elegido)
			
		spinner.bind(text=functionOne)	
		self.ids.Mercados.add_widget(spinner)

		frutas=[]
		with open('Frutas.txt',encoding="utf-8") as lineas:
			for linea in lineas:
				frutas.append(linea)
				
		
		spinner = Spinner(text='Frutas',values=frutas,
									size_hint_x= 0.25,size_hint_y= None,height=65,
									background_color= ( 0, 1, 0, 1),background_normal="down2.png",
									color=(0,0,0,.5))
		
		def functionTwo(spinner,text,**kwargs):
			global mercadoproducto_elegido
			global producto_elegido
			global producto 
			producto_elegido="Frutas"
			producto=text
			producto=producto.rstrip('\n')
			producto=producto.rstrip(' ') 
			mercadoproducto_elegido=str(mercado_elegido)+"_"+str(producto_elegido)+".csv"
			
			print(mercadoproducto_elegido)
			
		spinner.bind(text=functionTwo)
		self.ids.Productos.add_widget(spinner)
		


		hortalizas=[]
		with open('Hortalizas.txt',encoding="utf-8") as lineas:
			for linea in lineas:
				hortalizas.append(linea)
						
		spinner = Spinner(text='Hortalizas', 
									values=hortalizas,
									size_hint_x= 0.25,size_hint_y= None,height=65,
									background_color=( 10, 10, 0, 1),
									color=(0,0,0,.5))

		def functionThree(spinner,text):
			global mercadoproducto_elegido
			global producto_elegido
			global producto 
			producto_elegido="Hortalizas"
			producto=text
			producto=producto.rstrip('\n')
			producto=producto.rstrip(' ') 
			mercadoproducto_elegido=str(mercado_elegido)+"_"+str(producto_elegido)+".csv"
			
			print(mercadoproducto_elegido)
		spinner.bind(text=functionThree)
		self.ids.Productos.add_widget(spinner)					

		global chiles_secos
		chiles_secos=[]
		with open('Chiles Secos.txt',encoding="utf-8") as lineas:
			for linea in lineas:
				chiles_secos.append(linea)
						
		spinner = Spinner(text='Chiles Secos', 
									values=chiles_secos,
									size_hint_x= 0.25,size_hint_y= None,height=65,
									background_color= ( 0, 0, 1, 1),background_normal="down2.png",
									color=(0,0,0,.5))
		
		
		def functionFour(spinner,text):
			global mercadoproducto_elegido
			global producto_elegido
			global producto 
			producto_elegido='Chiles Secos'
			producto=text 
			producto=producto.rstrip('\n')
			producto=producto.rstrip(' ')
			mercadoproducto_elegido=str(mercado_elegido)+"_"+str(producto_elegido)+".csv"
			
			print()
			
		spinner.bind(text=functionFour)
		self.ids.Productos.add_widget(spinner)
		
		
		spinner = Spinner(markup = True,text='[color=F8F8FF]Periodo a analizar[/color]', 
									values=("Cuatro años", "Tres años", "Dos años", "Un año"),
									size_hint_x= 0.25,size_hint_y= None,height=65,
									background_color= ( 1, 0, 0, 1),
									color=(0,0,0,.5))
		
		
		def functionFive(spinner,text):
			global periodo_elegido
	
			
			periodo_elegido=text

					
			print(periodo_elegido)
			
		spinner.bind(text=functionFive)
		self.ids.Productos.add_widget(spinner)
		
		mybutton = Button(text= "Visualizar",size_hint_x= 0.25,
					size_hint_y=None, background_color=( .9372, .4980, 0.1019, 1),background_normal="down1.png",
					height=65)
		self.ids.Visualizar.add_widget(mybutton)
		mybutton.bind(on_press=self.visualizar)			
		
							
	def visualizar(self,event):

		with open(str(mercadoproducto_elegido),"r") as File:

			Filtros=[]
			for elemento in File:
				elemento=elemento.rstrip('\n')
				linea=elemento.split(";")
				if str(producto) in linea:
					Filtros.append([linea[0],linea[1],linea[2],linea[3],linea[4],linea[5],linea[6],linea[7]])

		if 'Cuatro años' in str(periodo_elegido):
			Fil=[]
			n=212
			Fil=Filtros[0:n+1]		
			print(Fil)
		elif 'Tres años' in str(periodo_elegido):
			Fil=[]
			n=159
			Fil=Filtros[0:n+1]		
			print(Fil)
		elif 'Dos años'	in str(periodo_elegido):
			Fil=[]
			n=106
			Fil=Filtros[0:n+1]		
			print(Fil)
		elif 'Un año' in str(periodo_elegido):
			Fil=[]
			n=53
			Fil=Filtros[0:n+1]		
			print(Fil)				
					
		with open("filtrado.csv", "w", newline="") as f:
			w=csv.writer(f)
			w.writerows(Fil)
		df=read_csv("filtrado.csv")
		df.columns=["FECHA","PRODUCTO","CLASE","CANTIDAD","ESTADO","MIN","PRECIO_PROMEDIO","MAX"]
		df.to_csv("filtra2.csv")
		
			
		sns.set(style="whitegrid")
		doc = pd.read_csv("filtra2.csv")
		sns_plot= sns.lineplot(x="FECHA", y="PRECIO_PROMEDIO",data=doc)
		fig = sns_plot.get_figure()
		fig.savefig("image1.png",transparent=True)
		picture = Image(source = 'image1.png')
		self.ids.Grafica.add_widget(picture)		
		print(mercadoproducto_elegido)
         
	
class Grafica1App(App):
	def build(self):
		return Caja()
		
			
if __name__ == '__main__':
    Grafica1App().run()
