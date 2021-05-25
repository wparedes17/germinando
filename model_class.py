# -*- coding: utf-8 -*-
"""
Created on Thu May  6 06:51:40 2021

@author: Wilfridovich
"""

import numpy as np

import datetime
import json

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

'''
En desarollo ya predice pero pero hay funciones que quizá deberían ser trasladas a market_products_structure
'''


class simple_model:
    
    def __init__(self, name, data, date):
        self.name = name
        self.raw_data = data
        self.last_update = date
        self.status = {}
        self.viability = {'Actual':False, 'Recurrente':False, 'Compatibilidad':False}
        self.period = {'Inicio':0, 'Fin':0}
        self.differences = {}
        self.probs = {}
        self.short_terms = {}
        
    def trustworthiness(self):
        day = datetime.date.today()
        year_reference = day.year
        
        #Es un producto que se mantiene en el SNIIM?
        if self.last_update.year >= year_reference-1:
            self.viability['Actual'] = True
        
        #Si está acutalmente en el SNIIM, tiene históricos suficientes?
        if self.viability['Actual'] == True:
            self.period['Inicio'] = 2009
            self.period['Fin'] = 2009
            for i in range(2009,year_reference+1):
                if str(i) in self.raw_data.prices:
                    self.period['Fin'] = i
                else:
                    self.period['Inicio'] = i+1
                    self.period['Fin'] = i+1
                    
            if self.period['Fin'] - self.period['Inicio'] > 5:
                self.viability['Recurrente'] = True
                
        #Hay compatibilidad verdadera? #Este fragmento se puede escribir más elegantemente
        aux = False
        if not self.raw_data.compatibility:
           for k,i in enumerate(self.raw_data.package.keys()):
               for h,j in enumerate(self.raw_data.package.keys()):
                   if h > k: 
                       if (i != j) and (self.raw_data.package[j]['Inicio'] >= self.raw_data.package[i]['Ultimo']):
                           self.viability['Compatibilidad'] = True
                       elif (i != j) and (self.raw_data.package[j]['Inicio'] < self.raw_data.package[i]['Ultimo']):
                            self.viability['Compatibilidad'] = False
                            aux = True
                            break
               if aux:
                   break
        else:
            self.viability['Compatibilidad'] = True
            
        
        #Si hay incompatibilidad, la incompatibilidad le resta históricos?
        if  (self.viability['Recurrente'] == True) and (not self.raw_data.compatibility):
            aux_date = datetime.datetime(2009, 1, 1)
            for i in self.raw_data.package.keys():
                if self.raw_data.package[i]['Inicio'] >= aux_date:
                    aux_date = self.raw_data.package[i]['Inicio']
            if self.period['Inicio'] < aux_date.year:
                self.period['Inicio'] = aux_date.year
            if self.period['Fin'] - self.period['Inicio'] > 5:
                self.viability['Recurrente'] = True

    
    def calculate_differences(self):
        for m in range(1,13):
            select_month = []
            self.probs[str(m)] = [0,0,0]
            for a in range(self.period['Inicio'],self.period['Fin']+1):
                try:
                    aux = [i for i in self.raw_data.prices[str(a)][str(m)]['Frecuente'] if i > 0]
                    select_month += [j-i for i,j in zip(aux[:-1],aux[1:])]
                except:
                    pass
            self.differences[str(m)] = np.array([abs(i) for i in select_month])
            self.probs[str(m)][0] = sum([1 for i in select_month if i > 0.0]) 
            self.probs[str(m)][1] = sum([1 for i in select_month if i == 0.0])
            self.probs[str(m)][2] = sum([1 for i in select_month if i < 0]) 
            if sum(self.probs[str(m)]) > 0:
                self.probs[str(m)] = np.array([i/sum(self.probs[str(m)]) for i in self.probs[str(m)]])
                self.status[str(m)] = True
            else:
                self.status[str(m)] = False
    
    def calculate_short_term(self):
        x = []
        y = []
        for m in range(1,13):
            select_month = []
            for a in range(self.period['Inicio'],self.period['Fin']+1):
                try:
                    select_month = [i for i in self.raw_data.prices[str(a)][str(m)]['Frecuente'] if i > 0]
                except:
                    pass
                if len(select_month) > 0:
                    y.append(np.mean(np.array(select_month)))
                    x.append(m)
        try:
            if len(set(x)) > 3:
                poly_reg = PolynomialFeatures(degree=2)
                x_poly = poly_reg.fit_transform(np.array(x).reshape((-1, 1)))
                trend_model = LinearRegression()
                trend_model.fit(x_poly,np.array(y))
                print(self.name,trend_model.coef_)
                self.short_terms = {'Status':1, 'Coeficientes':trend_model.coef_}
            else:
                self.short_terms = {'Status':0, 'Coeficientes':0}
        except:
            self.short_terms = {'Status':0, 'Coeficientes':0}
    
    def get_current_price(self):
        aux_date = self.last_update
        
        ref_price = 0.0
        ref_month = aux_date.month
        ref_day = aux_date.day
        ref_year = aux_date.year
        try:
            ref_price = self.raw_data.prices[str(ref_year)][str(ref_month)]['Frecuente'][ref_day-1]
        except:
            pass
        
        return ref_price, ref_day, ref_month, ref_year
    
    def make_one_simulation(self, window):
        aux_date = self.last_update
        ref_price, ref_month, ref_day, ref_year = self.get_current_price()
        
        predicted_price = ref_price

        for i in range(window):
            aux_date += datetime.timedelta(days=1)
            
            ref_day_name = aux_date.weekday()
            while ref_day_name >=5:
                aux_date = self.last_update + datetime.timedelta(days=1)
                ref_day_name = aux_date.weekday()
            
            ref_month = aux_date.month
            ref_day = aux_date.day
            
            if self.viability['Actual'] and self.viability['Recurrente'] and self.viability['Compatibilidad'] and self.status[str(ref_month)]:
                slope = np.random.rand()
                difference = np.random.exponential(np.mean(self.differences[str(ref_month)]))
                if slope < self.probs[str(ref_month)][0]:
                    predicted_price += difference
                elif slope > 1-self.probs[str(ref_month)][2]:
                    predicted_price -= difference
            else:
                if predicted_price != ref_price:
                    return ref_price, predicted_price, i+1
                else:
                    return 'Producto no disponible.\nPuede ser que sea un producto de temporada o que no se encuentre en nuestra base de datos', 0.0, 0.0
                
        return ref_price, predicted_price, window
    
    def make_prediction(self, window, n_iters=1000):
        expected_prediction = 0.0
        for i in range(n_iters):           
            ref_price, aux_prediction, current_window = self.make_one_simulation(window)
            expected_prediction += aux_prediction
        
        if isinstance(ref_price, str):
            return ref_price, 0.0, 0.0, 0.0
        else:
            return ref_price, expected_prediction/1000.0, expected_prediction/1000.0 - ref_price, current_window
        
    
class market_model:
    
    def __init__(self, name, date):
        self.name = name
        self.products = {}
        self.last_update = date
    
    def add_product(self, product_name, product_prices, date):
        if not product_name is self.products:
            self.products[product_name] = simple_model(product_name, product_prices, date)
        else:
            print('El modelo ya existe, ejecutar update')
            
    def export_product_names(self, ids):
        f = open(str(ids)+'/product_names.json', 'w')
        dict_to_export = {}
        for i in self.products.keys():
            if self.products[i].viability['Recurrente'] and self.products[i].viability['Actual'] and self.products[i].viability['Compatibilidad']:
                if i == 'Limón c/semilla # 5':
                    dict_to_export['limon'] = i
                else:
                    dict_to_export[i.lower()] = i
        dict_to_export['jitomate'] = 'Tomate Saladette'
        dict_to_export['tomatillo'] = 'Tomate Verde'
        dict_to_export['sandia'] = 'Sandía Rayada'
        dict_to_export['melon'] = 'Melón Cantaloupe sin clasificación'
        json.dump(dict_to_export, f)
        f.close()
        
    