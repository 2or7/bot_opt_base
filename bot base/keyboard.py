import types
from telebot import types

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('Водитель')
item2 = types.KeyboardButton('Арендатор')

markup.add(item1, item2)

menu = [
    [InlineKeyboardButton(text="Количество заявок", callback_data="app_number"),
    InlineKeyboardButton(text="Количество выданных пропусков", callback_data="passes_number")],
    [InlineKeyboardButton(text="Количество автомобилей на территории", callback_data="cars_number"),
    InlineKeyboardButton(text="Количество свободных мест для заезда", callback_data="places_number")],
    [InlineKeyboardButton(text="Количество завершенных заявок", callback_data="complited_app_number")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
