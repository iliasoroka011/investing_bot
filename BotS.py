# -*- coding: utf-8 -*-
import telebot
from telebot import types

import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import pandas as pd

token = "450574969:AAF-KNL1FkSEsLlDg0xuQJpkpvw4WLs-Y3Q"
bot = telebot.TeleBot(token)
stock_list = []
@bot.message_handler(func=lambda message: True, commands=['start'])
def Start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Инфо', 'Котировки')
    bot.send_message(message.chat.id, "Choose one letter:", reply_markup=markup)

@bot.message_handler(regexp="Инфо")
def info(message):
    types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "")

@bot.message_handler(regexp="Котировки")
def stocks(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Назад')
    markup.row(itembtn1)
    msg = bot.send_message(message.chat.id, "Введите тикер",reply_markup=markup)
    bot.register_next_step_handler(msg, stock_info)



def stock_info(message):
    msgj = message.text
    if str(msgj) == "Назад":
        msg = bot.send_message(message.chat.id, "Что дальше?")
        bot.register_next_step_handler(msg, Start)


    else:
        keyboard = types.InlineKeyboardMarkup()
        slovo = message.text
        ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
        data, meta_data = ts.get_intraday(slovo, interval='1min', outputsize='full')
        now = pd.DataFrame(data.tail(1))
        now1 = now['4. close']
        nw = str(now1)
        nw1 = nw[28:34]
        nw2 = float(nw1)
        openn = pd.DataFrame(data.head(1))
        openn1 = openn['1. open']
        op = str(openn1)
        op1 = op[28:34]
        op2 = float(op1)
        if nw2 >= op2:
            proc = round(100 - ((op2 / nw2) * 100), 2)
            proc1 = str(proc)
            bot.send_message(message.chat.id, slovo + " - $" + nw1 + ' +'+proc1+'%')
        elif nw2 < op2:
            proc = round(100 - ((nw2 / op2) * 100), 2)
            proc1 = str(proc)
            bot.send_message(message.chat.id, slovo + " - $" + nw1 + ' -'+proc1 + '%')

@bot.message_handler(regexp="k")
def currency(message):
    markup = types.ReplyKeyboardMarkup()
    itembtn1 = types.KeyboardButton('Назад')
    markup.row(itembtn1)
    msg = bot.send_message(message.chat.id, "Введите тикер",reply_markup=markup)
    bot.register_next_step_handler(msg, digital_currency)


def digital_currency(message):
    slovo = message.text
    ts = CryptoCurrencies(key='YOUR_API_KEY', output_format='pandas')
    data, meta_data = ts.get_digital_currency_intraday(slovo, market='CNY')
    now1 = data['5. Exchange Rate']
    bot.send_message(message.chat.id, now1)

if __name__ == '__main__':
     bot.polling(none_stop=True)