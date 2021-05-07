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
    f.close()
    
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

def estimate_model(ids):
    try:
        market_data_raw = load_data_structure(ids)
        market_models = create_simple_model(market_data_raw)

        f = open('28/simple_model.gdata','wb')
        pickle.dump(market_models, f)
        f.close()
        return 'Modelo estimado y guardado'

    except:
        return 'Algo falló'

def load_model(ids):
    f = open('28/simple_model.gdata','rb')
    market_models = pickle.load(f)
    f.close()

    return market_models

    
