# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 16:39:15 2019

@author: Erika
"""

from datetime import date, datetime, timedelta
import pandas as pd
from lxml import etree
import urllib 
import time

archivo = open("Nuevo Leon Mercado de Abasto Estrella de San Nicolas de los Garza_Hortalizas.csv","r")
last_record = archivo.readlines()[-1]
archivo.close()
fecha1 = last_record.split(",")
fecha_u=fecha1[0] 
print(fecha_u)
last = datetime.strptime(fecha_u, "%d/%m/%Y")

dia=timedelta(days=1)

formato = "%d/%m/%Y"
day1 = last+ dia
day = day1.strftime(formato) 
print(day)

today = date.today()
hoy = today.strftime("%d/%m/%Y")
print(hoy)


week_day = datetime.strptime(day, '%d/%m/%Y')
datetime.date(datetime_object).strftime("%V")

week_fecha_u = datetime.strptime(fecha_u, '%d/%m/%Y')
datetime.date(week_fecha_u).strftime("%V")

week_hoy = datetime.strptime(hoy, '%d/%m/%Y')
datetime.date(week_hoy).strftime("%V")