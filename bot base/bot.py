import telebot
import config
import keyboard
import main
import text
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, text.welcome.format(message.from_user, bot.get_me()), parse_mode='html',
                     reply_markup=keyboard.markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text_to_handle = message.text.lower()

    if text_to_handle == 'арендатор':
        bot.send_message(message.chat.id, 'Введите логин')
        bot.register_next_step_handler(message, input_login)


def input_login(message):
    global login
    login = message.text
    flag_login = 0
    rentor_id = None

    for l in main.rentors:
        if login == l["LOGIN"]:
            rentor_id = l["ID"]
            flag_login = 1
            print(main.rentors[rentor_id]["PASSWORD"])
            bot.send_message(message.chat.id, text.user_found)
            bot.register_next_step_handler(message, input_password, rentor_id)

    if flag_login != 1:
        bot.send_message(message.chat.id, text.login_retry)

def input_password(message, rentor_id):
    global password
    password = message.text
    global flag_password
    flag_password = 0

    if password == main.rentors[rentor_id]["PASSWORD"]:
        bot.send_message(message.chat.id, "Вход выполнен")
        send_second_menu(message.chat.id)  # Отправляем вторую клавиатуру
        flag_password = 1

    if flag_password != 1:
        bot.send_message(message.chat.id, text.password_retry)

def send_second_menu(chat_id):
    # Создайте клавиатуру для второго меню
    bot.send_message(chat_id, "Выберите действие: ", reply_markup=keyboard.second_menu_keyboard)

bot.polling(none_stop=True)