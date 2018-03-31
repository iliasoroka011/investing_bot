import telebot
from yahoo_finance import Share
from yahoo_finance import Currency

token = "330646368:AAEWEv5qq3t2psZOs-32ACnUm3NEBnu02Ug"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def functions_handler(message):
    bot.send_message(message.chat.id, "Здравствуйте")
    bot.send_message(message.chat.id, "Соберем портфель?")
    if ((message.text == "Да") or (message.text == "да" )):
        bot.send_message(message.chat.id, "ок")

