# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 14:01:41 2019

@author: jacob
"""
import pandas as pd

from lxml import etree
import urllib

import datetime

import time

#Función para cargar la base de datos de opciones
def load_market_database():
    return pd.read_csv("Mercados_ID.csv")

#Descarga la tabla para un mercado y día específico
def get_day(target, date):
    address1 = "http://www.economia-sniim.gob.mx/NUEVO/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ResultadosConsultaFechaFrutasYHortalizas.aspx?fechaInicio="
    address2 = "&fechaFinal="
    address3 = "&ProductoId=-1&OrigenId=-1&Origen=Todos&DestinoId="
    address4 = "&PreciosPorId=1&RegistrosPorPagina=500"
    
    address = address1 + date + address2 + date + address3 + str(target.ID) + "&Destino=" + target.Cadena + address4

    ## Carga el sitio y lo decodifica en utf-8
    web = urllib.request.urlopen(address)
    s = web.read()
    s = s.decode("utf8")

    html = etree.HTML(s)

    ## Encuentra todos los 'tr', la tabla se llama tblResultados, puede cambiar con
    ## el tiempo
    tr_nodes = html.xpath('//table[@id="tblResultados"]/tr')
    
    if len(tr_nodes) < 1:
        return ""
    else:
        header = [i[0].text for i in tr_nodes[0].xpath("th")]
        td_content = [[td.text for td in tr.xpath('td')] for tr in tr_nodes[1:]]
        return td_content

#Almacena los datos obtenidos en una tabla, además regresa un valor de éxito o fracaso
#con base en si hubo o no datos
def save_day(target,date,html_data):
    if len(html_data) > 0:
        for hortaliza in html_data:
            if len(hortaliza) < 2:
                try:
                    archivo.close()
                except:
                    pass
                tipo = hortaliza[0]
                nombre = target.Mercado+"_"+tipo+".csv"
                archivo = open(nombre,"a+")
            if len(hortaliza) > 1:
                linea = date
                for i in range(len(hortaliza)-1):
                    try:
                        linea += ","+hortaliza[i].replace(",","")
                    except:
                        linea += ","+"NO DISPONIBLE"
                try:
                    archivo.write(linea+"\n")
                except:
                    archivo = open(target.Mercado+"_Sin categoría"+".csv","a+")
                    archivo.write(linea+"\n")
        archivo.close()
        return "exito"
    else:
        return "fracaso"

#Genera un archivo de registro para los días de exito
def log_day(target,date,status):
    nombre = target.Mercado+"_registro.txt"
    archivo = open(nombre,"a+")
    archivo.write(date+"\t"+status+"\n")
    archivo.close()

#Genera la fecha de ayer con base en la fecha de hoy
def next_day(today):
    step = datetime.timedelta(days=1)
    return today+step

#Inicio y fin del periodo de búsqueda
day = datetime.datetime(2009, 1, 1)
end_day = datetime.datetime(2019, 3, 13)

max_tries = 3
time_delay = 5

#Descarga automática
market = load_market_database()


for i in range(28,29):
    day = datetime.datetime(2009, 1, 1)
    while day < end_day:
        print(day)
        ok = 0
        number_try = 1
        
        while ok == 0 and number_try < max_tries:
            try:
                day_data = get_day(market.loc[i],day.strftime('%d/%m/%Y'))
                ok = 1
            except:
                number_try += 1
                print("Upss! Algo salió mal, volveré a intentar. Intento no. "+str(number_try))
                time.sleep(time_delay)
        
        day_status = save_day(market.loc[i],day.strftime('%d/%m/%Y'),day_data)
        log_day(market.loc[i],day.strftime('%d/%m/%Y'),day_status)
        day = next_day(day)
