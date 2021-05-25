# -*- coding: utf-8 -*-
"""
Created on Sun May  2 12:33:26 2021

@author: Wilfridovich
"""
import simple_model as smm
import natural_processing as nlp
import numpy as np
import telebot
import datetime
import re

model = smm.load_model(28)

bot = telebot.TeleBot("TOKEN", parse_mode='HTML') # You can set parse_mode by default. HTML or MARKDOWN

def validate_command(command):
    if command['instruccion'] is None:
        return False
    elif (not command['producto'] is None) and (not command['mercado'] is None):
        if command['instruccion'] == 'resumen':
            return True
        elif not command['auxiliares'] is None:
            return True
    else:
        return False


def process_command(string):
    if re.search(r'@.*', string):
        orden = {'instruccion':None, 'producto':None, 'mercado':None, 'auxiliares':None}
        window_names = {'mes':30, 'meses':30, 'semana':7, 'semanas':7,'año':365, 'años':365, 'dia':1, 'dias':1}
        try:
            aux = re.search('^[a-z]+\s', string[1:].lower())
            orden['instruccion'] = aux.group()[:-1]
            
            aux = nlp.delete_accent_mark(string[(aux.end()+1):].lower()).split('en')
            orden['mercado'] = nlp.identify_market([re.search(r'[a-z]+', aux[1]).group()],nlp.market_names_natural)
            orden['producto'] = [nlp.idenfy_product([i for i in aux[0].split() if i != ''], j) for j in orden['mercado']]
            
            if orden['instruccion'] == 'precio':
                orden['auxiliares'] = {'fecha':[int(i) for i in re.search(r'[0-9]+.*', aux[1]).group().split('-')]}
            elif orden['instruccion'] == 'compara':
                orden['auxiliares'] = {'precio':float(re.search(r'[0-9]+.*', aux[1]).group())}
            elif orden['instruccion'] == 'predice':
                orden['auxiliares'] = {'ventana':int(re.search(r'[0-9]+', aux[1]).group()), 'longitud':window_names[aux[1].split()[-1]]}
            else:
                orden['auxiliares'] = None       
            
            return orden
        
        except:
            return {'instruccion':None, 'producto':None, 'mercado':None, 'auxiliares':None}     
            
    else:
        return nlp.understanding(string.lower())
    


def date_to_window(model, date, name_product):
    model_date = model.products[name_product].last_update 
    target_date = datetime.datetime(date[2], date[1], date[0])
    
    return (target_date-model_date).days


def action_forecast(model, ids, orden):
    answer = ''
    if len(orden['producto'][ids]) > 1:
        answer += 'La instrucción contiene más de un producto. Te muestro lo que encontré:\n\n'
    
    for i in orden['producto'][ids]:
        print(i)
        try:
            answer += '<b>'+model.products[i].name+'</b>\n'
            if 'fecha' in orden['auxiliares']:
                pred = model.products[i].make_prediction(date_to_window(model, orden['auxiliares']['fecha'], i))
            else:
                pred = model.products[i].make_prediction(orden['auxiliares']['ventana']*orden['auxiliares']['longitud'])
            
            if isinstance(pred[0], str):
                answer += ' -- No disponiblle para predicción\n\n'
            else:
                pred = [round(i, 2) for i in pred]
                if pred[2] > 0:
                    answer += 'Se espera un incremento para dentro de ' + str(pred[3]) + ' días después del ' + model.products[i].last_update.strftime('%d/%m/%Y') + '\n\n'
                    answer += 'Incremento esperado de ' + str(pred[2]) +' MXN\n\n'
                else:
                    answer += 'Se espera un decremento para dentro de ' + str(pred[3]) + ' días después del ' + model.products[i].last_update.strftime('%d/%m/%Y') + ' es de:\n\n'  
                    answer += str(-pred[2])+'\n\n'
                answer += 'Hoy está a '+ str(pred[0]) + ' MXN y llegará a' + str(pred[1]) + ' MXN\n\n'
        except:
            answer += i+' -- No disponible en el mercado\n\n'
        
        answer += '----------\n'
    
    return answer

def action_summary(model, ids, orden):
    meses = {1:'Enero', 2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', 7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}
    answer = ''
    if len(orden['producto'][ids]) > 1:
        answer += 'La instrucción contiene más de un producto. Te muestro lo que encontré:\n\n'
    
    for i in orden['producto'][ids]:
        try:
            answer += '<b>'+model.products[i].name+'</b>\n'
            current_price, aux_1, aux_2, aux_3 = model.products[i].get_current_price()
            aux_ref_y = datetime.date.today().year
            aux_ref_m = datetime.date.today().month
            if (aux_ref_y == aux_3) and(aux_ref_m == aux_2):
                answer += 'El precio al ' + model.products[i].last_update.strftime('%d/%m/%Y') + ' es de ' + str(round(current_price,2))+'\n\n'
                if model.products[i].short_terms['Status'] == 1:
                    coefs = model.products[i].short_terms['Coeficientes']
                    for c in coefs:
                        print(c)
                    maximo = int(round(-coefs[1]/(2*coefs[2])))
                    if (coefs[2] < 0) and (maximo in meses):
                        answer += 'Los precios más altos se encuentran alrededor del mes de:  ' + meses[maximo]+'\n'
                        answer += 'El producto tiene un comportamiento temporal'+'\n'
                        diff = (11*coefs[1]+143*coefs[2])/current_price*100
                        answer += '\nAdemás su precio presenta '  + str(round(diff,2)) + '% de incremento anual'+'\n'  
                    elif (coefs[2] < 0) and (coefs[1] < 0):
                        answer += 'Los precios más altos se encuentran alrededor del mes de:  Enero\n'
                        answer += 'Los precios descienden a lo largo de año'+'\n'
                    elif (coefs[2] > 0) and (maximo in meses):
                        answer += 'Los precios más bajos se encuentran alrededor del mes de:  ' + meses[maximo]+'\n'
                        answer += 'Los precios más altos usualmente ocurren al final del año de mes por la inflación'+'\n'
                        diff = (11*coefs[1]+143*coefs[2])/current_price*100
                        answer += '\nAdemás su precio presenta '  + str(round(diff,2)) + '% de incremento anual'+'\n'  
                    
                else:
                     answer += i+' -- No disponible en el mercado\n\n'
            else:
                 answer += i+' -- No disponible en el mercado\n\n'
        except:
             answer += i+' -- No disponible en el mercado\n\n'
        answer += '----------\n'
    
    return answer
    
            
def make_action(string):
    print(string)
    action_command = process_command(string)
    print(action_command)
    do_action = validate_command(action_command)
    
    if do_action:
        message_answer = ''
        for k, mkt in enumerate(action_command['mercado']):
            try:
                market = smm.load_model(mkt)
                if action_command['instruccion'] == 'predice':
                    message_answer += market.name+'\n'
                    message_answer += action_forecast(market, k, action_command)
                elif action_command['instruccion'] == 'resumen':
                    message_answer += market.name+'\n'
                    message_answer += action_summary(market, k, action_command)
                else:
                    message_answer += 'De momento no puedo responder de momento.'
            except:
                message_answer += mkt + '  -- Mercado no disponible. Pero pronto estará\n\n'
    else:
        message_answer = 'No te entendí, pero aprendo cada día más.\n\nPuedes mandar lo que escribiste a bitbot.services@gmail.com'
    
    return message_answer

        
        

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hola, soy el Bot de Germinando!\n\nEscribe lo que desees saber sobre los mercados de Frutas y Hortalizas del país.\n\nPuedes redactarlo como creas conveniente aunque como no usamos tu ubicación siempre indica el estado del país de la consulta. \n\n Por ejemplo, puedes probar escribiendo: 'en cuanto anda el aguacate en queretaro?' \n\nSi no logro entenderte puedes usar /help para conocer las ordenes específicas")


@bot.message_handler(commands=['help'])
def send_help(message):
    if message.text == '/help':
        bot.reply_to(message, '''Nuestra idea es que no requieras las ordenes específicas.
Pero si no te arroja el resultado deseado, puede intentar usarlas.

Hay 4 ordenes específicas: 
1. Resumen -- No necesita auxiliares
2. Precio -- Auxiliares: Fecha en formato DD-MM-AAAA               
3. Predice -- Auxiliares: Ventana Longitud            
4. Compara -- Auxiliares: Precio por kilogramo/unidad
              
La estructura de una orden es: @Orden + Producto + EN + Mercado + Auxiliares. Algunos ejemplos:    
1. @Resumen Aguacate Hass en Querétaro
2. @Precio Aguacate Hass en Queretaro 17-04-2020               
3. @Predice Aguacate Hass en Queretaro 7 días             
4. @Compara Aguacate Hass en Queretaro 40
''')
    else:
        bot.reply_to(message, "Disculpa, me siguen capacitando.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, make_action(message.text))
    
        

	


bot.polling()
