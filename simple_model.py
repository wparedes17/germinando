# -*- coding: utf-8 -*-
"""
Created on Wed May  5 09:54:43 2021

@author: Wilfridovich
"""

import market_products_structure as mps
import model_class as mc

import pickle


"""
load_data_structure
    Input: local_id --- número entre 0 y 45 de acuerdo a nuestra listas de mercados. Por ejemplo Qro es el 28.
    Output: Carga de los datos en bruto obtenidos por el bot
"""
def load_data_structure(ids):
    f = mps.load_market_information(ids)
    market_obj = pickle.load(f)
    
    return market_obj

"""
Create_simple_model
    Input: market_prices_raw --- estructura de datos del bot con los datos en bruto.
    Output: market simple model --- estructura de datos con el modelo para cada uno de los productos viables.
"""
def create_simple_model(market_prices_raw):
    market_simple_model = mc.market_model(market_prices_raw.name, market_prices_raw.last_update)
    for i in market_prices_raw.products.keys():
        market_simple_model.add_product(i, market_prices_raw.products[i], market_prices_raw.products[i].last_update)
        market_simple_model.products[i].trustworthiness()
        market_simple_model.products[i].calculate_differences()
    
    return market_simple_model



market_data_raw = load_data_structure(28)
market_models = create_simple_model(market_data_raw)

test_r = market_models.products['Aguacate Hass']
print(test_r.make_prediction(14))
