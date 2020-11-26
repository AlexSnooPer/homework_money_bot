import telebot
from config import keys, TOKEN
from extention import APIException, MoneyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def starter(message: telebot.types.Message):
    text = f'Приветствую, {message.chat.username}! \
\nСписок доступных комманд:\nПомощь: /help\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def helper(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите мне комманду в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \
\nНапример, если вы хотите перевести 20 долларов в рубли напишите:\nдоллар рубль 20 \
\nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        money_values = message.text.split(' ')

        if len(money_values) != 3:
            raise APIException("Введен некорректный запрос")

        quote, base, amount = money_values
        total_base = MoneyConverter.get_price(quote, base, amount)
        money_date = MoneyConverter.get_date(quote, base)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя,\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base} на дату {money_date}'
        bot.reply_to(message, text)


bot.polling()
