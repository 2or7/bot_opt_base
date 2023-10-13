from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from driver_handlers import cursor, conn
import random
from datetime import datetime, timedelta

import keyboards as kb
import database as db
import driver_handlers as dh

rt_router = Router()


class Form_for_auth(StatesGroup):
    login_process = State()
    password_process = State()
    auth_finished = State()


class Form_for_search_car(StatesGroup):
    plate_process = State()

    
@rt_router.message(F.text == 'Арендатор')
async def message_to_input_login(message: Message, state: FSMContext):
    await message.answer(f'Введите логин', reply_markup=kb.back)
    await state.set_state(Form_for_auth.login_process)


@rt_router.message(Form_for_auth.login_process)
async def input_login(message: Message, state: FSMContext):
    login = message.text
    flag_login = 0
    global rentor_id
    for l in db.rentors:
        if login == l["LOGIN"]:
            rentor_id = l["ID"]
            flag_login = 1
            await message.answer(f'Пользователь найден! Введите пароль.', reply_markup=kb.back)
            await state.set_state(Form_for_auth.password_process)
    if flag_login != 1:
        await message.reply("Пользователь не найден! Поробуйте ещё раз.\n\n При возникновении вопросов, нажмите /help", reply_markup=kb.back)
        return


@rt_router.message(Form_for_auth.password_process)
async def input_password(message: Message, state: FSMContext):
    password = message.text
    if password == db.rentors[rentor_id]["PASSWORD"]:
        current_time = datetime.now()
        cursor.execute("INSERT INTO users (full_name, passport_number, user_type, event_time, chat_id_temp, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                            str(message.from_user.first_name + ' ' + message.from_user.last_name), 
                            [str(password)],
                            False,
                            current_time, 
                            message.from_user.id, 
                            dh.number
                        )
                        )
        conn.commit()
        await message.answer(f'Вход выполнен. {db.rentors[rentor_id]["NAME"]}', reply_markup=kb.rentors)
        await state.set_state(Form_for_auth.auth_finished)
    else:
        await message.reply("Неверный пароль! Поробуйте ещё раз. \n\n При возникновении вопросов, нажмите /help", reply_markup=kb.back)
        return


@rt_router.message(F.text == 'Всего заявок')
async def info(message: Message):
    await message.answer(f'Всего заявок: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Пропусков выдано')
async def info(message: Message):
    await message.answer(f'Пропусков выдано: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Автомобилей на территории')
async def info(message: Message):
    await message.answer(f'Автомобилей на территории: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Свободных мест')
async def info(message: Message):
    await message.answer(f'Свободных мест: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Заявок завершено')
async def info(message: Message):
    await message.answer(f'Заявок завершено: {random.randint(10, 50)}')


@rt_router.message(F.text == 'Информация по заявке')
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
