from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram import types
main_kb = [
    [KeyboardButton(text='Арендатор'),
     KeyboardButton(text='Водитель')]
]

main = ReplyKeyboardMarkup(keyboard=main_kb,
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже: ')

socials_kb = [
    [InlineKeyboardButton(text='Telegram', url='https://t.me/ggggfhk')],
    [InlineKeyboardButton(text='Vk', url='https://vk.com/id362483811')]
]

socials = InlineKeyboardMarkup(inline_keyboard=socials_kb)

back_kb = [
    [KeyboardButton(text='Вернуться в главное меню')]
]

back = ReplyKeyboardMarkup(keyboard=back_kb,
                           resize_keyboard=True)

drivers_info = [
    [KeyboardButton(text='Данные о заявке'),
     KeyboardButton(text='Кол-во машин на территории')],
    [KeyboardButton(text='Кол-во машин в очереди'),
     KeyboardButton(text='Вернуться в главное меню')],
]

drivers = ReplyKeyboardMarkup(keyboard=drivers_info,
                              resize_keyboard=True,
                              input_field_placeholder='Выберите один из пунктов меню: ')

rentors_info = [
    [KeyboardButton(text='Всего заявок'),
     KeyboardButton(text='Пропусков выдано')],
    [KeyboardButton(text='Автомобилей на территории'),
     KeyboardButton(text='Свободных мест')],
    [KeyboardButton(text='Заявок завершено'),
     KeyboardButton(text='Информация по заявке')],
    [KeyboardButton(text='Вернуться в главное меню')]
]

rentors = ReplyKeyboardMarkup(keyboard=rentors_info,
                              resize_keyboard=True,
                              input_field_placeholder='Выберите пункт ниже: ')

share_button = [
    [KeyboardButton(text = 'Отправьте свой номер телефона', request_contact=True)]
                ]
share_keyboard = types.ReplyKeyboardMarkup(keyboard=share_button, resize_keyboard=True, one_time_keyboard=True)

