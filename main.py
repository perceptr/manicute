import telebot
from telebot import types  # для указание типов
import picture

bot = telebot.TeleBot('5768637891:AAFXvKfqu0Dip25TnKs06ZeQx0Rt8_etizs')


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💅 Ноготочки")
    btn2 = types.KeyboardButton("💅 Педикюр")
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id,
                     "Привет, {0.first_name}!\nЯ - {1.first_name}, бот созданный для того, чтобы ты мог(ла) "
                     "посмотреть на красивые ноготочки.".format(
                         message.from_user, bot.get_me()), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "💅 Ноготочки":
        bot.send_photo(message.chat.id, picture.get_manicure_link())
    elif message.text == "💅 Педикюр":
        bot.send_photo(message.chat.id, picture.get_pedicure_link())
    else:
        bot.send_message(message.chat.id, text="Я не знаю такой команды!")


bot.polling(none_stop=True)
