from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main_kb = [
    [KeyboardButton(text='Арендатор'),
     KeyboardButton(text='Водитель')],
    [KeyboardButton(text='Контакты'),
    KeyboardButton(text='Помощь')]
]

main = ReplyKeyboardMarkup(keyboard=main_kb,
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже: ')

socials_kb = [
    [InlineKeyboardButton(text='Telegram', url='https://t.me/ggggfhk')],
    [InlineKeyboardButton(text='Vk', url='https://vk.com/id362483811')]
]

socials = InlineKeyboardMarkup(inline_keyboard=socials_kb)
