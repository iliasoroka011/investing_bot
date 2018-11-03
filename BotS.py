# -*- coding: utf-8 -*-
import telebot

from telebot import types
from alphaVantageAPI.alphavantage import AlphaVantage
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import pyplot
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
from alpha_vantage.foreignexchange import ForeignExchange
from newsapi import NewsApiClient

AV = AlphaVantage(api_key='ZBRM5PCHPIYQV8BY', output_size='full', output='pandas')

token = "450574969:AAF-KNL1FkSEsLlDg0xuQJpkpvw4WLs-Y3Q"
bot = telebot.TeleBot(token)
items = []
@bot.message_handler(func=lambda message: True, commands=['start'])
def Start(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('Информация о боте', 'Котировки','Форекс','Портфель')
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

@bot.message_handler(regexp="Назад")
def back(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('Информация о боте', 'Котировки','Форекс','Портфель')
        bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

@bot.message_handler(regexp="Информация о боте")
def info(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('Котировки', 'Форекс', 'Портфель', 'Назад')
        bot.send_message(message.chat.id, "Вас приветствует бот - инвестиционный помощник.")
        bot.send_message(message.chat.id, "Функции функции которые я умею выполнять: 1. Отправлять вам информацию об акции 2. Отправлять вам информацию о валютной паре 3. Составлять портфель акций")
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

@bot.message_handler(regexp="Котировки")
def stocks(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('Apple','Tesla','Microsoft','Nike')
        markup.row('Starbucks', 'NVIDIA', 'Tesla', 'Intel')
        markup.row("Назад")
        msg = bot.send_message(message.chat.id, "Введите название акции или выберите из списка:",reply_markup=markup)
        bot.register_next_step_handler(msg, stock_info)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)


def stock_info(message):
    try:
        text = message.text
        if text == "Назад":
            markup = types.ReplyKeyboardMarkup()
            markup.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup()
            markup.row("Получить новости", "Добавить акцию", "Назад")
            global slovo
            global ticket
            slovo = message.text
            Ndata = AV.search(slovo)
            Ndata1 = pd.DataFrame(Ndata.head(1))
            global name
            ticket = Ndata1['1. symbol'][0]

            name = Ndata1['2. name'][0]
            ts = TimeSeries(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
            data, meta_data = ts.get_intraday(ticket, interval='1min', outputsize='full')
            dat, meta_dat = ts.get_daily(ticket, outputsize='full')
            now = pd.DataFrame(data.tail(1))
            now1 = now['4. close']
            nw = str(now1)
            nw1 = nw[28:34]
            nw2 = float(nw1)
            openn = pd.DataFrame(dat.tail(2))
            openn1 = openn['4. close']
            op = str(openn1)
            op1 = op[19:23]
            op2 = float(op1)

            if nw2 >= op2:
                proc = round(100 - ((op2 / nw2) * 100), 2)
                proc1 = str(proc)
                bot.send_message(message.chat.id, name + " - $" + nw1 + ' +' + proc1 + '%')
            elif nw2 < op2:
                proc2 = round(100 - ((nw2 / op2) * 100), 2)
                proc2 = str(proc2)
                bot.send_message(message.chat.id, name + " - $" + nw1 + ' -' + proc2 + '%')
            da, meta_data = ts.get_intraday(ticket, outputsize='full', interval='1min')
            da['4. close'].plot()

            plt.title('Intraday Times Series (1min) within 10 days')
            plt.savefig('graph.png')
            plt.close()
            photo = open("graph.png", 'rb')
            bot.send_photo(message.chat.id, photo)
            msg = bot.send_message(message.chat.id, "Что дальше?", reply_markup=markup)
            bot.register_next_step_handler(msg, news)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)


def news(message):
    try:
        text = message.text
        if text == "Назад":
            mar = types.ReplyKeyboardMarkup()
            mar.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=mar)
        elif text == "Добавить акцию":
            markup = types.ReplyKeyboardMarkup()
            markup.row("Получить новости", "Назад")
            items.append(ticket)
            print(items)
            mes = bot.send_message(message.chat.id,"Акция добавлена", reply_markup=markup)
            bot.register_next_step_handler(mes, news_next)
        elif text == "Получить новости":
            mark = types.ReplyKeyboardMarkup()
            mark.row("Добавить акцию", "Назад")
            t =0
            newsapi = NewsApiClient(api_key='cfa09a3adc7f47eab3d72f016392e170')
            n = newsapi.get_everything(q=name,
                               language='en',
                               sort_by='publishedAt',
                               page_size=4,
                               page=1)
            while t < len(n['articles']):
                bot.send_message(message.chat.id, (n['articles'][t]['url']))
                t += 1
            msg = bot.send_message(message.chat.id, "Новости получены", reply_markup=mark)
            bot.register_next_step_handler(msg, news_next)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

def news_next(message):
    try:
        text = message.text
        if text == "Назад":
            markup = types.ReplyKeyboardMarkup()
            markup.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

        if text == "Добавить акцию":
            markup = types.ReplyKeyboardMarkup()
            markup.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            items.append(ticket)
            bot.send_message(message.chat.id,"Акция добавлена", reply_markup=markup)

        elif text == "Получить новости":
            mark = types.ReplyKeyboardMarkup()
            mark.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            t =0
            newsapi = NewsApiClient(api_key='cfa09a3adc7f47eab3d72f016392e170')
            n = newsapi.get_everything(q=name,
                               language='en',
                               sort_by='publishedAt',
                               page_size=4,
                               page=1)
            while t < len(n['articles']):
                bot.send_message(message.chat.id, (n['articles'][t]['url']))
                t += 1
            msg = bot.send_message(message.chat.id, "Новости показаны", reply_markup=mark)

    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

@bot.message_handler(regexp="Форекс")
def currency(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('USD-RUB', 'RUB-USD', 'USD-EUR', 'EUR-USD')
        markup.row('EUR-GBP', 'GBP-EUR', 'CHF-EUR', 'EUR-CHF')
        markup.row("Назад")
        msg = bot.send_message(message.chat.id, "Введите тикер(в формате ...-... , где точки это тикет валюты) или выберете из списка", reply_markup=markup)
        bot.register_next_step_handler(msg, digital_currency)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)


def digital_currency(message):
    try:
        text = message.text
        if text =="Назад":
            markup = types.ReplyKeyboardMarkup()
            markup.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup()
            markup.row("Получить новости", "Назад")
            global slov
            slov = message.text
            String = str(slov)
            string1 = String[0:3]
            string2 = String[4:7]
            cc = ForeignExchange(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
            # There is no metadata in this call
            data, meta_data = cc.get_currency_exchange_daily(from_symbol=string1, to_symbol=string2, outputsize='full')
            now = pd.DataFrame(data.tail(1))
            now1 = now['1. open']
            nw = str(now1)
            nw2 = nw[19:25]
            nw3 = float(nw2)
            openn = pd.DataFrame(data.tail(1))
            openn1 = openn['4. close']
            op = str(openn1)
            op2 = op[19:25]
            op3 = float(op2)
            if op3 >= nw3:
                proc = round(100 - ((op3 / nw3) * 100), 2)
                proc1 = str(proc)
                bot.send_message(message.chat.id, slov + " - $" + op2 + ' +' + proc1 + '%')
            elif op3 < nw3:
                proc2 = round(100 - ((nw3 / op3) * 100), 2)
                proc2 = str(proc2)
                bot.send_message(message.chat.id, slov + " - $" + op2 + ' -' + proc2 + '%')
            da, meta_data = cc.get_currency_exchange_daily(from_symbol=string1, to_symbol=string2, outputsize='full')
            da['4. close'].plot()

            plt.title('Intraday Times Series (1 min) within 10 days')
            plt.savefig('graph.png')
            plt.close()
            photo = open("graph.png", 'rb')
            bot.send_photo(message.chat.id, photo)
            msg = bot.send_message(message.chat.id, "Получить новости?", reply_markup=markup)
            bot.register_next_step_handler(msg, new)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

def new(message):
    try:
        text = message.text
        if text == "Получить новости":
            mark = types.ReplyKeyboardMarkup()
            mark.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            t =0
            newsapi = NewsApiClient(api_key='cfa09a3adc7f47eab3d72f016392e170')
            n = newsapi.get_everything(q=slov,
                               language='en',
                               sort_by='publishedAt',
                               page_size=4,
                               page=1)
            while t < len(n['articles']):
                bot.send_message(message.chat.id, (n['articles'][t]['url']))
                t += 1
            bot.send_message(message.chat.id, "Новости получены", reply_markup=mark)
        elif text == "Назад":
            mar = types.ReplyKeyboardMarkup()
            mar.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=mar)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

@bot.message_handler(regexp="Портфель")
def start_watchlist(message):
    try:
        markup = types.ReplyKeyboardMarkup()
        markup.row('Посмотреть портфель', 'Настройки')
        markup.row("Назад")
        msge = bot.send_message(message.chat.id, "Действия с портфелем:", reply_markup=markup )
        bot.register_next_step_handler(msge, next_step_watchlist)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

def next_step_watchlist(message):
    try:
        text = message.text
        if text == "Настройки":
            markup = types.ReplyKeyboardMarkup()
            markup.row('Добавить акцию', 'Очистить портфель', 'Удалить по названию')
            markup.row("Назад")
            msge = bot.send_message(message.chat.id, "Что хотите настроить?", reply_markup=markup)
            bot.register_next_step_handler(msge, settings)
        elif text == "Посмотреть портфель":
            ts = TimeSeries(key='ZBRM5PCHPIYQV8BY', output_format='pandas')
            markup = types.ReplyKeyboardMarkup()
            markup.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            for x in items:

                Ndata = AV.search(x)
                Ndata1 = pd.DataFrame(Ndata.head(1))
                ticket = Ndata1['1. symbol'][0]
                name = Ndata1['2. name'][0]
                data, meta_data = ts.get_intraday(ticket, interval='1min', outputsize='full')
                dat, meta_dat = ts.get_daily(ticket, outputsize='full')
                now = pd.DataFrame(data.tail(1))
                now1 = now['4. close']
                nw = str(now1)
                nw1 = nw[28:34]
                nw2 = float(nw1)
                openn = pd.DataFrame(dat.tail(2))
                openn1 = openn['4. close']
                op = str(openn1)
                op1 = op[19:23]
                op2 = float(op1)
                if nw2 >= op2:
                    proc = round(100 - ((op2 / nw2) * 100), 2)
                    proc1 = str(proc)
                    bot.send_message(message.chat.id, name + " - $" + nw1 + ' +' + proc1 + '%')
                elif nw2 < op2:
                    proc = round(100 - ((nw2 / op2) * 100), 2)
                    proc1 = str(proc)
                    bot.send_message(message.chat.id, name + " - $" + nw1 + ' -' + proc1 + '%')
            msge = bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        elif text == "Назад":
            mar = types.ReplyKeyboardMarkup()
            mar.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=mar)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)
def settings(message):
    try:
        text = message.text
        if text == "Добавить акцию":
            msge = bot.send_message(message.chat.id, "Введите тикет/название" )
            bot.register_next_step_handler(msge, add_ticket)
        elif text == "Очистить портфель":
            m = types.ReplyKeyboardMarkup()
            m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            items.clear()
            msg = bot.send_message(message.chat.id, "removed", reply_markup=m)
        elif text == "Удалить по названию":
                msg = bot.send_message(message.chat.id, "write stock that should be deleted")
                bot.register_next_step_handler(msg, del_stock)
        elif text == "Назад":
            mar = types.ReplyKeyboardMarkup()
            mar.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=mar)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)
def del_stock(message):
    try:
        mar = types.ReplyKeyboardMarkup()
        mar.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        dlsT = message.text
        Ndata = AV.search(dlsT)
        Ndata1 = pd.DataFrame(Ndata.head(1))
        ticket = Ndata1['1. symbol'][0]
        for i in items:
            if i == ticket:
                items.remove(i)
                bot.send_message(message.chat.id, "Акция удалена", reply_markup=mar)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)

def add_ticket(message):
    try:
        mar = types.ReplyKeyboardMarkup()
        mar.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        global items
        item = message.text
        Ndata = AV.search(item)
        Ndata1 = pd.DataFrame(Ndata.head(1))
        ticket = Ndata1['1. symbol'][0]
        items.append(ticket)
        bot.send_message(message.chat.id, "Акция добавлена", reply_markup=mar)
    except Exception as e:
        m = types.ReplyKeyboardMarkup()
        m.row('Информация о боте', 'Котировки', 'Форекс', 'Портфель')
        bot.send_message(message.chat.id, 'Что-то пошло не так...', reply_markup=m)


if __name__ == '__main__':
     bot.polling(none_stop=True)