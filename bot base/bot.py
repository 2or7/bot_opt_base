from aiogram.types import Message
import telebot
import config
import main
import text
import keyboard
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, text.welcome.format(message.from_user, bot.get_me()), parse_mode='html',
                     reply_markup=keyboard.markup)


@bot.message_handler(content_types=['text'])
def request_l_p(message):
    if message.text == 'Арендатор':
        bot.send_message(message.chat.id, 'Введите логин')
        bot.register_next_step_handler(message, input_login)


def input_login(message):
    global login
    login = message.text
    flag_login = 0
    rentor_id = None  # Изменим имя переменной, чтобы избежать конфликта с встроенными именами
    for l in main.rentors:
        if login == l["LOGIN"]:
            rentor_id = l["ID"]
            flag_login = 1
            print(main.rentors[rentor_id]["PASSWORD"])
            bot.send_message(message.chat.id, text.user_found)
            bot.register_next_step_handler(message, input_password,
                                           rentor_id)  # Передадим rentor_id как аргумент в следующую функцию
    if flag_login != 1:
        bot.send_message(message.chat.id, text.login_retry)


def input_password(message, rentor_id):  # Добавим аргумент rentor_id
    global password
    password = message.text
    global flag_password
    flag_password = 0
    if password == main.rentors[rentor_id]["PASSWORD"]:
        bot.send_message(message.chat.id, "Вход выполнен")
        flag_password = 1
    if flag_password != 1:
        bot.send_message(message.chat.id, text.password_retry)


@bot.message_handler(content_types=["text"])
def result_of_login(message):
    bot.send_message(message.chat.id, "Ф")


bot.polling(none_stop=True)
