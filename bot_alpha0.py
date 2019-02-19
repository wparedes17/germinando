# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 23:32:03 2019

@author: jacob
"""

from lxml import etree
import urllib

import pandas as pd

## Carga una tabla de las opciones de mercados existentes
market = pd.read_csv("Mercados_ID.csv")

## Genera la dirección de búsqueda
address1 = "http://www.economia-sniim.gob.mx/NUEVO/Consultas/MercadosNacionales/PreciosDeMercado/Agricolas/ResultadosConsultaFechaFrutasYHortalizas.aspx?fechaInicio="
date = "18/02/2019"
address2 = "&fechaFinal="
address3 = "&ProductoId=-1&OrigenId=-1&Origen=Todos&DestinoId="
address4 = "&PreciosPorId=1&RegistrosPorPagina=500"

address = address1 + date + address2 + date + address3 + str(market.ID[0]) + "&Destino=" + market.Cadena[0] + address4

## Carga el sitio y lo decodifica en utf-8
web = urllib.request.urlopen(address)
s = web.read()
s = s.decode("utf8")

html = etree.HTML(s)

## Encuentra todos los 'tr', la tabla se llama tblResultados, puede cambiar con
## el tiempo
tr_nodes = html.xpath('//table[@id="tblResultados"]/tr')

## Encuenta los nodos de la tabla
header = [i[0].text for i in tr_nodes[0].xpath("th")]

## Encuentra los datos
td_content = [[td.text for td in tr.xpath('td')] for tr in tr_nodes[1:]]


for hortaliza in td_content:
    if len(hortaliza) < 2:
        try:
            archivo.close()
        except:
            pass
        tipo = hortaliza[0]
        nombre = market.Mercado[0]+"_"+tipo+".csv"
        archivo = open(nombre,"a+")
    if len(hortaliza) > 1:
        linea = date
        for i in range(len(hortaliza)-1):
            linea += ","+hortaliza[i]
        archivo.write(linea+"\n")

archivo.close()
















