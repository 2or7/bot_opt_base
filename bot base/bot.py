import telebot
import config
import main

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Водитель")
    item2 = types.KeyboardButton("Арендатор")

    markup.add(item1, item2)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы упростить систему ввоза и вывоза грузов с оптовой базы.\nНажмите на кнопку, которая соответсвует вашему статусу.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def request_l_p(message):
    if message.text == 'Арендатор':
        bot.send_message(message.chat.id, 'Введите логин')
        @bot.message_handler(content_types=['text'])
        def input_login(message):
            global login
            login = message.text
            flag_login = 0
            for l in main.rentors:
                if(login == l["LOGIN"]):
                    id = l["ID"]
                    flag_login = 1
                    print(main.rentors[id]["PASSWORD"])
                    bot.send_message(message.chat.id, "Пользователь найден. Введите пароль")
                    @bot.message_handler(content_types=['text'])
                    def input_password(message):
                        global input_password
                        password = message.text
                        flag_password = 0
                        
                        if(password == main.rentors[id]["PASSWORD"]):

                            bot.send_message(message.chat.id, "Вход выполнен")
                            flag_password = 1
                        if(flag_password != 1):
                            bot.send_message(message.chat.id, "Вы неправильно ввели пароль. Нажмите на кнопку /start для того, чтобы повторить попытку")
                    bot.register_next_step_handler(message, input_password)
            if(flag_login != 1):
                bot.send_message(message.chat.id, "Такого логина не существует. Нажмите на кнопку /start для того, чтобы повторить попытку")
        bot.register_next_step_handler(message, input_login)



bot.polling(none_stop=True)