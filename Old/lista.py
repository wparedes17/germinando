from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

import time
import os

FechaHoy=time.strftime("%d/%m/%y")
with open("selecciones.txt","r+") as archivo:
    if os.stat("selecciones.txt").st_size == 0:
     print("Vacío")
    else: 
        parrafo= [(columna.rstrip().split(" ")) for columna in archivo]
        for i in parrafo:
            U=i[-1]
            Fecha=U[14:22]
            if Fecha==FechaHoy:
                Estado="Actualizado"
            else:
                Estado="No Actualizado"
ListaGlobal=[]
nombres=open("Nombres.txt","r")
with open("lista.kv", encoding='utf8') as f:
            Builder.load_string(f.read())

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index])
            variable=("mercado: {0}".format(rv.data[index])+"//"+Estado+ "//ultima fecha de actualización:"+FechaHoy+'\n')
            ListaGlobal.append(variable)
        else:
            print("selection removed for {0}".format(rv.data[index]))
    def button_selection(self):
            for i in ListaGlobal:   
                with open("selecciones.txt","a+") as archivo:
                    archivo.write(i)

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = [{'text': str(x)} for x in nombres]


class TestApp(App):
    def build(self):
        return RV()

if __name__ == '__main__':
    TestApp().run()
