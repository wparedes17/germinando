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



with open("ejemplo.kv", encoding='utf8') as f:
            Builder.load_string(f.read())
dicbig= {}
def diccionario():
    bigrama=[]
    with open("Nombres.txt","r") as lista:
        new_record=lista.readlines()
        for i in new_record:
            KD=i[-3:-1]
            Dc=i[:-4]
            contador=0
            for s in Dc: 
                contador+=1    
                if s==":":
                    Estado=Dc[:contador-1]
            bigrama.append([KD,Dc,Estado])  

    for mercado in bigrama: 
        KeyDic= mercado[2]#Las llaves son el nombre del estado
        Dic=mercado[1] #Nombre de mercado
        if dicbig.get(KeyDic)== None:
            dicbig[KeyDic]=Dic 
        else:
            dicbig[KeyDic]=Dic+";"+dicbig.get(KeyDic)#agrega la frecuencia de la misma llave
diccionario()
ListaGlobal=[]
Texto=[]


class Test(Screen):
    gender = StringProperty("")
    selected = BooleanProperty(True)
    def descargar_data(self):
       if self.selected == True:
            print("Estado={0}".format(self.gender))
            variable="{0}".format(self.gender)
            ListaGlobal.append(variable)
            print(ListaGlobal)
            elegido=variable
            for key in dicbig:
                if key==elegido:
                    texto=dicbig[key]
                    Texto.append(texto)
                    print(Texto)

    def button_selection(self):
            for i in ListaGlobal:   
                with open("selecciones.txt","a+") as archivo:
                    archivo.write(i)

    def mostrar_mercados(self):
        elegido=ListaGlobal[0]
        for key in dicbig:
            if key==elegido:
                print(dicbig[key])


class SettingsScreen(Screen):
    pass



# Create the screen manager
sm = ScreenManager()
sm.add_widget(Test(name='menu'))
sm.add_widget(SettingsScreen(name='settings'))


class MyApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()