# -*- coding: utf-8 -*-
"""
Created on Fri May  7 22:22:51 2021

@author: Wilfridovich
"""

import datetime
import json
import re


stop_json = open("stopwords-es.json",'r', encoding='utf-8')
stop_words = json.load(stop_json)
stop_json.close()

markets_json = open("mercado_names.json",'r', encoding='utf-8')
market_names_natural = json.loads(markets_json.read())
markets_json.close()


#Recibida la expresión natural, creamos limpia reducida, estas funciones lo hacen
def identify_question(string):
    questions = {'cuanto':1, 'cual':2, 'como':3, 'que':4}

    for i,j in questions.items():
        expression = re.compile('[\s0-9a-z]*'+i+'[\s0-9a-z]*')
        if re.match(expression, string):
            return j, re.sub(i+'\\s', '', string)
        
    return 5, string

def delete_accent_mark(string):
    vocals = {'á':'a', 'é':'e', 'í':'i','ó':'o','ú':'u'}
    filtered_string = string
    for i,j in vocals.items():
        filtered_string = re.sub(i, j, filtered_string)        
    
    return filtered_string

def delete_symbols(string):       
    return re.sub(r'[^a-z0-9/\-\.\s]', '', string)

def simple_tokenization(string):
    return re.sub(r'[\s]+', ' ', string).split(' ')

def simple_clean(tokens):
    return [i for i in tokens if (not i in stop_words) and (i != '')]




#Lo primero primero, es encontrar el mercado de consulta, todas las consultas deben dar un mercado de consulta
def delete_vowels(string):
    return re.sub(r'[aeiou]', '', string)
       

def search_abbreviations(tokens, vocabulary, mode=(1,0)):
    coincidences = {}
    for i in tokens:
        if (mode[0] == 1):
            aux_i = delete_vowels(i)
        else:
            aux_i = i
        for j in vocabulary.keys():
            if mode[1] == 1:
                aux_j = delete_vowels(j)
            else:
                aux_j = j
            if re.search('\\b'+aux_i+'\\s', aux_j+' '):
                if aux_j in coincidences:
                    coincidences[j] += 1
                else:
                    coincidences[j] = 1
    return coincidences

def select_result(results, vocabulary):
    if len(results.keys()) == 1:
        return vocabulary[list(results.keys())[0]]

    elif len(results.keys()) > 1:
        ref = 0
        for i,j in results.items():
            if j > ref:
                ref = j
                selected_key = vocabulary[i]
        
        if ref >= 1:
            return selected_key
        else:
            return 'Error'
    
    else:
        return 'Error'


def identify_market(tokens, vocabulary):
    search_results = search_abbreviations(tokens, vocabulary)
    
    return select_result(search_results, vocabulary)
    

def idenfy_product(tokens, ids):
    try:
        products_json = open(str(ids)+"/product_names.json",'r', encoding='utf-8')
        product_names = json.load(products_json)
        products_json.close()
    except:
        return 'Error: Mercado identificado pero no disponible para consulta'
    
    search_results = search_abbreviations(tokens, product_names, (0,0))
    best_results = max(search_results.values())
    
    return [product_names[i] for i,j in search_results.items() if j == best_results]

def identify_window(token, phrase):
    window_names = {'mes':30, 'meses':30, 'semana':7, 'semanas':7,'año':365, 'años':365, 'dia':1, 'dias':1}
    for i in token:
        if i in window_names:
            if ('un' in token) or ('una' in token):
                return {'ventana':1, 'longitud':window_names[i]}
            else:
                aux = re.search(r'[0-9]', phrase)
                if aux:
                    return {'ventana':int(aux.group()), 'longitud':window_names[i]}
                else:
                    return {'ventana':0, 'longitud':window_names[i]}
    
    aux = re.search('[0-9]+[/-][0-9]+[/-][0-9]+', phrase)
    if aux:
        return {'fecha_f':aux.group()}
    else:
        aux = re.search(r'[0-9]+ de [a-z]+\s?d?e?l?\s?[0-9]*', phrase)
        if aux:
            return {'fecha_n':aux.group()}
        else:
            return None
  
def identify_price(phrase):
    try:
        return {'precio':float(re.search(r'[0-9]+\.?[0-9]*', phrase).group())}
    except:
        return None     



#Esta es la función que se encarga mandar llamar a las funciones
#en el orden requerido para transformar una petición natura
#en una petición bot
def understanding(phrase):
    orden = {'instruccion':None, 'producto':None, 'mercado':None, 'auxiliares':None}

    #La frase final es la frase tokenizada. 
    filtered_phrase = delete_accent_mark(phrase)
    filtered_phrase = delete_symbols(filtered_phrase)

    type_question, filtered_phrase = identify_question(filtered_phrase)

    token_phrase = simple_clean(simple_tokenization(filtered_phrase))
    

    orden['mercado'] = identify_market(token_phrase, market_names_natural)
    orden['producto'] = [idenfy_product(token_phrase, i) for i in orden['mercado']]
    orden['auxiliares'] = identify_window(token_phrase, filtered_phrase)
    if orden['auxiliares'] is None:
         orden['auxiliares'] = identify_price(filtered_phrase)
         if orden['auxiliares'] is None:
             if re.search('ayer', filtered_phrase):
                 orden['instruccion'] = 'precio'
                 orden['auxiliares'] = {'ventana':1, 'longitud':1}
                 return orden
             elif re.search('mañana', filtered_phrase):
                 orden['instruccion'] = 'predice'
                 orden['auxiliares'] = {'ventana':1, 'longitud':1}       
                 return orden
             else:
                 orden['instruccion']= 'resumen'
                 return orden
         else:
             orden['instruccion']= 'compara'
             return orden
         
    elif 'fecha_f' in orden['auxiliares']:
        if re.search('/', orden['auxiliares']['fecha_f']):
            aux_1 = [int(i) for i in orden['auxiliares']['fecha_f'].split('/')]
            aux_2 = datetime.datetime(aux_1[2], aux_1[1], aux_1[0])
            orden['auxiliares'] = {'fecha':aux_1}
            if aux_2 > datetime.datetime(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day):
                orden['instruccion']= 'predice'
                return orden
            else:
                orden['instruccion']= 'precio'
                return orden
    
    elif 'fecha_n' in orden['auxiliares']:
        month_names = {'enero':1, 'febrero':2, 'marzo':3, 'abril':4, 'mayo':5, 'junio':6, 'julio':7, 'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre':11, 'diciembre':12}
        aux_1 = re.sub(r'[0-9\s]+', '', orden['auxiliares']['fecha_n'])
        aux_2 = [int(i) for i in re.findall(r'[0-9]+', '', orden['auxiliares']['fecha_n'])]
        aux_3 = [0,0,0]
        for i in month_names:
            if re.search(aux_1, i):
                aux_3[1] = month_names[i]
        if len(aux_2) < 2:
            aux_3[2] = datetime.date.today().year
        else:
            aux_3[0] = aux_2[0]
            aux_3[2] = aux_2[1]
        
        aux_4 = datetime.datetime(aux_1[2], aux_1[1], aux_1[0])
        if aux_4 > datetime.datetime(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day):
            orden['instruccion'] = 'predice'
            return orden
        else:
            orden['instruccion'] = 'precio'
            return orden
    
    else:
        keywords = ['fue','hace','estuvo','anduvo']
        for i in token_phrase:
            if i in keywords:
                orden['instruccion'] = 'precio'
                return orden
            else:
                orden['instruccion'] = 'predice'
                return orden
            
