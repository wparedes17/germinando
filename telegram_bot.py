# -*- coding: utf-8 -*-
"""
Created on Sun May  2 12:33:26 2021

@author: Wilfridovich
"""
import simple_model as smm
import numpy as np
import telebot
import datetime
import re

model = smm.load_model(28)
order_dict = {'predice':1, 'resumen':2, 'compara':3, 'precios':4}

bot = telebot.TeleBot("1739935286:AAEmk8V4o_GxR3Deo0Nxu0bvuT4uBun3WGA", parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

def get_command_parameters(string, task):
    if task == 1:
        try:
            element_location = re.search(r'[^0-9]+', string).span()
            product = re.sub(r'\A[\s]+', '', string[element_location[0]:element_location[1]])
            product = re.sub(r'\b[a-z]', lambda m: m.group().upper(), product)
            product = product.strip()
        except:
            return 'Producto no encontrado'
        try:
            window = int(re.search(r'[0-9]+', string[element_location[1]:]).group())
        except:
            return 'Longitud de ventana no encontrada'
        
        return product, window

def process_command(string, commands = order_dict):
    element_location = re.search(r'[\s]*[^\s]+', string).span()
    if string[element_location[0]:element_location[1]].lower() in commands:
        task = commands[string[element_location[0]:element_location[1]].lower()]
        parameters  = get_command_parameters(string[element_location[1]:], task)
        if (task == 1) and (parameters[0] in model.products):
            pred = model.products[parameters[0]].make_prediction(parameters[1])
            if isinstance(pred[0], str):
                return pred[0]
            else:
                pred = [round(i, 2) for i in pred]
            if pred[2] > 0:
                answer = 'Se espera un incremento para dentro de ' + str(pred[3]) + ' días después del ' + model.products[parameters[0]].last_update.strftime('%d/%m/%Y') + '\n\n'
                answer += 'Incremento esperado de ' + str(pred[2]) +' MXN\n\n'
            else:
                answer = 'Se espera un incremento para dentro de ' + str(pred[3]) + ' días después del ' + model.products[parameters[0]].last_update.strftime('%d/%m/%Y') + ' es de:\n\n'  
                answer += str(-pred[2])+'\n\n'
            answer += 'Pasando de '+ str(pred[0]) + ' MXN  a ' + str(pred[1]) + ' MXN'
            
            if parameters[1] > pred[3]:
                answer += '\n\nNota: No fue posible hacer la predicción completa.\Se presenta una predicción reducida.'
            return answer
        
        else:
            return 'Producto no encontrado. Puede intentar nuevamente'
            
    else:
        return '¡Lo siento, no te entendí!'
        
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hola, soy el Bot de Germinando!\n\nEscribe lo que desees saber sobre los mercados de Frutas y Hortalizas.\n\nPuedes redactarlo como creas conveniente. Pero como sigo aprendiendo, si no logro entenderte puedes usar /help para conocer los comandos específicos")

@bot.message_handler(commands=['help'])
def send_help(message):
    if message.text == '/help':
        bot.reply_to(message, '''Comandos específicos:
1. Resumen Nombre del producto Mercado. 
Ejemplo: Resumen Jitomate Querétaro. 
                        
2. Precios Nombre del producto Mercado
Ejemplo: Precios Jitomate Querétaro
                         
3. Predice Nombre del producto Ventana Mercado.
Ejemplo: Predice Jitomate 4 semanas Querétaro
                    
4. Compara Nombre del producto Precio Mercado. 
Ejemplo: Compara Jitomate 9.50 Querétaro
                         
Los comandos especificos tienen funciones adicionales, puedes escribir /help Compara para saber más sobre el comando especifico Compara.''')
    else:
        bot.reply_to(message, "Disculpa, me siguen capacitando.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, process_command(message.text))
    
        

	


bot.polling()
