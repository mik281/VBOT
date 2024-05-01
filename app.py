import telebot
from config import keys, TOKEN
from Extentions import ConvrtionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Для того чтобы начать, введите в строку ввода команду в следующем формате (без переноса не следующую строку): \n<имя валюты, из которой хотите перевести>\n<имя валюты, в которую хотите перевести>\n<кол-во переводимой валюты>\nУвидеть список всех доступнух валют можно с помощью команды /values\nВалюты, название котрых состоит из двух слов, нужно записывать через знак "_", например: канадский_доллар'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
     values = message.text.split(' ')

     if len(values) != 3:
         raise ConvrtionException('Слишком много параметров, обратите внимание на формат ввода, описанный в инструкции /help')

     quote, base, amount = values
     total_base = CryptoConverter.convert(quote, base, amount)
    except ConvrtionException as e:
         bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
     text = f'Цена {amount} {quote} в {base} = {total_base}({keys[base]})'
     bot.send_message(message.chat.id, text)

bot.polling()
