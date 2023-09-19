from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main_kb = [
    [KeyboardButton(text='Арендатор'),
     KeyboardButton(text='Водитель')],
    [KeyboardButton(text='Помощь')]
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
    [InlineKeyboardButton(text='Назад')]
]

back = InlineKeyboardMarkup(inline_keyboard=back_kb)


drivers_info = [
    [KeyboardButton(text='Сведения о заявке'),
     KeyboardButton(text='Кол-во машин на территории')],
    [KeyboardButton(text='Кол-во машин в очереди'),
     KeyboardButton(text='Помощь')],
]

drivers = ReplyKeyboardMarkup(keyboard=drivers_info,
                              resize_keyboard=True,
                              input_field_placeholder='Выберите один из пунктов меню: ')


rentors_info = [
    [KeyboardButton(text='Общее количество заявок'),
     KeyboardButton(text='Количество выданных пропусков')],
     [KeyboardButton(text='Количесвто автомобилей на территории'),
      KeyboardButton(text='Количесвто свободных мест')],
      [KeyboardButton(text='Количество завершённых заявок'),
       KeyboardButton(text='Детальные данные по конкретному автомобилю')],
       [KeyboardButton(text='Помощь')]
]

rentors = ReplyKeyboardMarkup(keyboard=rentors_info,
                           resize_keyboard=True,
                           input_field_placeholder='Выберите пункт ниже: ')

