# -*- coding: utf-8 -*-

#Libreri­as con nombres cortos
import urllib.request as ur #Manejo de las peticiones al SNIIM
import pandas as pd #Manejo de archivos csv

#Libreri­as con nombre completo
import datetime # Manejo de fecha
import pickle #Manejo de la estructura de datos: carga y guardado
import time #Manejo de tiempo de espera para controlar peticiones
import re #Manejo del texto recolectado

#Funciones especi­ficas de liberi­as
from lxml import etree #Acomodo de estructura de la informacion del SNIIM


#Mercados del SNIIM de acuerdo a su ID y Nombre de Mercado
#Obtenido del sitio del SNIIM en su codigo fuente
def load_market_database():
    return pd.read_csv("SNIIM_files/Mercados_ID.csv", sep=',')


"""
load_market_information
    Input: local_id --- número entre 0 y 45 de acuerdo a nuestra listas de mercados. Por ejemplo Qro es el 28.
    Output: 0 si no hay archivo local, el archivo si existe. El archivo tiene una estructura de datos con la informacion en bruto indi­zada
"""
def load_market_information(local_id):
    try:
        f = open(str(local_id)+'/information.gdata', 'rb')
        return f
    except:
        return 0

"""
get_day
    Input: 
        target. Una fila de un data.frame pandas con la informacion del mercado: su ID y CADENA con la que el SNIIM lo busca
        ddte. Una fecha en formato texto en formato D/M/ANO
    Output: Una lista con los resultados si es que existen.
"""
def get_day(target, date):
    #Solicitud al SNIIM
    address1 = "http://www.economia-sniim.gob.mx/NUEVO/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ResultadosConsultaFechaFrutasYHortalizas.aspx?fechaInicio="
    address2 = "&fechaFinal="
    address3 = "&ProductoId=-1&OrigenId=-1&Origen=Todos&DestinoId="
    address4 = "&PreciosPorId=1&RegistrosPorPagina=500"

    address = address1 + date + address2 + date + address3 + str(target.ID) + "&Destino=" + target.Cadena + address4
    ## Carga el sitio y lo decodifica en utf-8
    web = ur.urlopen(address)
    s = web.read()
    s = s.decode('utf8')
    html = etree.HTML(s)

    ## Encuentra todos los 'tr', la tabla se llama tblResultados, puede cambiar con
    ## el tiempo
    tr_nodes = html.xpath('//table[@id="tblResultados"]/tr')

    if len(tr_nodes) < 1:
        return ''
    else:
        header = [i[0].text for i in tr_nodes[0].xpath("th")]
        td_content = [[td.text for td in tr.xpath('td')] for tr in tr_nodes[1:]]
        return td_content


"""
box_package
    Input: 
        string_box. Una cadena con el tipo de empacado. Por ejemplo: Manojo, Docena, Caja 30 kg.
    Output: 
        Una tupla de 2 elementos: factor de conversion y clasificacion de conversion.
"""
def box_package(string_box):
    string_box = string_box.lower()
    if string_box == "kilogramo":
        return 1.0, "Convertible A"
    elif string_box == "docena":
        return 12.0, "Convertible B"
    elif (string_box == "pieza") or (string_box == "manojo"):
        return 1.0, "Convertible B"
    else:
        temp = re.findall(r'[0-9]+\s*kg', string_box)
        if len(temp) > 0:
            temp = re.findall(r'[0-9]+\s*kg', string_box)[0]
            return float(re.findall(r'[0-9]+', temp)[0]), "Convertible A"
        else:
            return 1.0, "Convertible N"

"""
next_day
    Input: 
        today. Una fecha en formato datetime
    Output: 
        Una fecha en formato datetime con los datos del di­a siguiente.
"""
def next_day(today):
    step = datetime.timedelta(days=1)
    return today+step


"""
Clase producto: Estructura de datos para manejar los productos.

    Posee 3 metodos:
        1. add_data.                        
        2. make_record. Procesar la informacion en bruto y actualizar la estructura
        3. update_compatibility. Revisa la fidelidad de los precios debido a conversion.
        
    Posee la siguiente informacion:
        1. Historicos resumidos de origenes
        2. Historicos resumidos de calidad
        3. Historicos resumidos de presentacion
        4. Historicos diarios indizados de precios
"""
class product:    
    def __init__(self, name, date):
        self.name = name
        self.origin = {}
        self.prices = {}
        self.quality = {}
        self.last_update = date
        self.raw_data = []
        self.package = {}
        self.compatibility = True
        self.status = 0
        
    def add_data(self, data, date):
        self.raw_data = data
        self.status = 1
        self.last_update = date
                
        
    def make_record(self):
        if self.status != 0:
            #Actualizamos el origen
            if not self.raw_data[2] in self.origin:
                self.origin[self.raw_data[2]] = {'Inicio':self.last_update, 'Ultimo':self.last_update}
            else:
                self.origin[self.raw_data[2]]['Ultimo'] = self.last_update
    
            #Actualizamos la calidad
            if not self.raw_data[0] in self.quality:
                self.quality[self.raw_data[0]] = {'Inicio':self.last_update, 'Ultimo':self.last_update}
            else:
                self.quality[self.raw_data[0]]['Ultimo'] = self.last_update
    
            #Actualizamos el tipo de empacado
            factor_price, type_price = box_package(self.raw_data[1])
            if not type_price in self.package:
                self.package[type_price] = {'Inicio':self.last_update, 'Ultimo':self.last_update}
            else:
                self.package[type_price]['Ultimo'] = self.last_update
    
            #Actualizamos los precios
            aux_prices = [re.sub(',', '', i) for i in self.raw_data[3:6]]
            aux_prices = [float(i)/factor_price for i in aux_prices]
            aux = [str(self.last_update.year), str(self.last_update.month), self.last_update.day]
            
            if not aux[0] in self.prices:
                self.prices[aux[0]] = {}
            if not aux[1] in self.prices[aux[0]]:
                self.prices[aux[0]][aux[1]] = {'Frecuente':[0 for i in range(31)],'Minimo':[0 for i in range(31)],'Maximo':[0 for i in range(31)]}
                
            self.prices[aux[0]][aux[1]]['Frecuente'][aux[2]-1] = aux_prices[2]
            self.prices[aux[0]][aux[1]]['Minimo'][aux[2]-1] = aux_prices[0]
            self.prices[aux[0]][aux[1]]['Maximo'][aux[2]-1] = aux_prices[1]
            
            self.raw_data = []
            self.status = 0
            
    def update_compatibility(self):
        if len(self.package.keys()) > 1:
            self.compatibility = False
            
"""
Clase producto: Estructura de datos para manejar los productos.

    Posee 3 metodos:
        1. make_logs. Genera un registro sobre si se tiene informacion del di­a o no.
        2. add_record. Adicionar informacion en bruto y registra que hay informacion sin procesar.
        3. make_records. Procesa la informacion y actualiza la lista de productos existentes
        
    Posee la siguiente informacion:
        1. Nombre del mercado
        2. Resumen vacÃ­o
        3. Listado indizado de todos los productos que se han vendido alguna vez en el mercado desde la fecha 2009-01-01
        4. Registro de si se tiene los datos de un di­a especi­fico
        5. Fecha de ultima actualizacion
"""        
class market:
    
    def __init__(self, name, date):
        self.name = name
        self.summary = {}
        self.products = {}
        self.logs = {}
        self.last_update = date
        self.last_record_raw = []
        self.status = 0
    
    def make_logs(self, date=None):
        if date is None:            
            aux = [str(self.last_update.year), str(self.last_update.month), str(self.last_update.day)]
        else:
            aux = [str(date.year), str(date.month), str(date.day)]
            self.last_update = date
              
        if not aux[0] in self.logs:
            self.logs[aux[0]] = {}
        if not aux[1] in self.logs[aux[0]]:
            self.logs[aux[0]][aux[1]] = {}
        if not aux[2] in self.logs[aux[0]][aux[1]]:
            self.logs[aux[0]][aux[1]][aux[2]] = 0
        
        del aux
    
    def add_record(self, data):
        aux = [str(self.last_update.year), str(self.last_update.month), str(self.last_update.day)]
        if len(data) > 0:
            self.last_record_raw = data
            self.logs[aux[0]][aux[1]][aux[2]] = 1
            self.status = 1
        else: 
            self.status = 0
            
        del aux
    
    def make_records(self):
        if self.status != 0:
            for p in self.last_record_raw:
                if len(p) > 1:
                    if not p[0] in self.products:
                        self.products[p[0]] = product(p[0], self.last_update)
                    self.products[p[0]].add_data(p[1:], self.last_update)
                    self.products[p[0]].make_record()
                    self.products[p[0]].update_compatibility()
                    
                    
         

            