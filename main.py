import telebot
from extensions import APIException, Converter
from config import keys, TOKEN


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = (f'/start или /help - справка\n'
            '/values - доступные валюты\n'
        'Введите сообщение боту в виде <имя валюты, '
        'цену которой нужно узнать> <имя валюты '
        'в которой надо узнать цену первой валюты> ' 
        '<количество первой валюты>')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text='Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values =  message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неверное колличество параметров.')
        quote, base, amount = values
        quote = quote.lower()
        base = base.lower()
        total_base=Converter.get_price(quote,base,amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} : {total_base}'
        bot.send_message(message.chat.id,text)


bot.polling()