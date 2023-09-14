import types
from telebot import types

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Водитель')
item2 = types.KeyboardButton('Арендатор')

markup.add(item1, item2)

# Определите клавиатуру для второго меню
second_menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
second_menu1 = types.KeyboardButton("Количество заявок")
second_menu2 = types.KeyboardButton("Количество выданных пропусков")
second_menu3 = types.KeyboardButton("Количество автомобилей на территории")
second_menu4 = types.KeyboardButton("Количество свободных мест для заезда")
second_menu5 = types.KeyboardButton("Количество завершенных заявок")

second_menu_keyboard.add(second_menu1, second_menu2, second_menu3, second_menu4, second_menu5)

