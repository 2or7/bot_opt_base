from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import random
from datetime import datetime, timedelta

import keyboards as kb
import database as db

rt_router = Router()


class Form_for_auth(StatesGroup):
    start_state = State()
    login_process = State()
    password_process = State()
    auth_finished = State()


class Form_for_search_car(StatesGroup):
    plate_process = State()

    
@rt_router.message(F.text == 'Арендатор')
async def message_to_input_login(message: Message, state: FSMContext):
    await message.answer(f'Введите логин', reply_markup=kb.back)
    if not message.text == 'Назад':
        await state.set_state(Form_for_auth.login_process)
    else:
        await state.set_state(Form_for_auth.start_state)


@rt_router.message(Form_for_auth.login_process)
async def input_login(message: Message, state: FSMContext):
    login = message.text
    flag_login = 0
    global rentor_id
    for l in db.rentors:
        if login == l["LOGIN"]:
            rentor_id = l["ID"]
            flag_login = 1
            await message.answer(f'Пользователь найден! Введите пароль.')
            await state.set_state(Form_for_auth.password_process)
    if flag_login != 1:
        await message.reply("Пользователь не найден! Поробуйте ещё раз.\n\n При возникновении вопросов, нажмите /help")
        return


@rt_router.message(Form_for_auth.password_process)
async def input_password(message: Message, state: FSMContext):
    password = message.text
    flag_password = 0
    if password == db.rentors[rentor_id]["PASSWORD"]:
        await message.answer(f'Вход выполнен', reply_markup=kb.rentors)
        flag_password = 1
        await state.set_state(Form_for_auth.auth_finished)
    if flag_password != 1:
        await message.reply("Неверный пароль! Поробуйте ещё раз. \n\n При возникновении вопросов, нажмите /help")
        return


@rt_router.message(F.text == 'Общее количество заявок')
async def info(message: Message):
    await message.answer(f'Общее количество заявок: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Количество выданных пропусков')
async def info(message: Message):
    await message.answer(f'Количество выданных пропусков: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Количесвто автомобилей на территории')
async def info(message: Message):
    await message.answer(f'Количесвто автомобилей на территории: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Количесвто свободных мест')
async def info(message: Message):
    await message.answer(f'Количесвто свободных мест: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Количество завершённых заявок')
async def info(message: Message):
    await message.answer(f'Количество завершённых заявок: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Детальные данные по конкретному автомобилю')
async def input_plate(message: Message, state: FSMContext):
    await message.answer(f'Введите госномер автомобиля')
    await state.set_state(Form_for_search_car.plate_process)


@rt_router.message(Form_for_search_car.plate_process)
async def detaile_info(message: Message):
    plate = message.text
    flag_plate = 0
    for d in db.drivers:
        if plate == d["VEHICLE_PLATE"]:
            flag_plate = 1
            await message.answer(f"Информация о человеке:\n"
                                 f"Полное имя: {d['FULL_NAME']}\n"
                                 f"Номер автомобиля: {d['VEHICLE_PLATE']}\n"
                                 f"Тип автомобиля: {d['VEHICLE_TYPE']}\n"
                                 f"Состояние разрешения: {d['PERMIT_STATE']}")
    if flag_plate != 1:
        await message.reply("Автомобиля нет в базе данных. Попробуйте еще раз. \n\n При возникновении вопросов, нажмите /help")
        return
