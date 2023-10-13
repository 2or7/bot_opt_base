from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


import random
from datetime import datetime, timedelta

import keyboards as kb
import database as db
import psycopg2

conn = psycopg2.connect(dbname='opt_base', user='postgres', password='postgres', host='127.0.0.1')

cursor = conn.cursor()

router = Router()

class Driver(StatesGroup):
    passport_finished = State()
    driver_data = State()


@router.message(Command("start", ignore_case=True))
async def cmd_start(message: Message, state: FSMContext):
    await message.reply("Привет, чтобы отправить мне свой номер телефона, нажмите на кнопку ниже.",
                        reply_markup=kb.share_keyboard, parse_mode='HTML')
    
@router.message(lambda message: message.contact is not None)
async def start_2(message: Message, state: FSMContext):
    temp = str(message.contact.phone_number)

    global number
    number = temp[1:]
    print(number)
    chat_id = str(message.from_user.id)

    

    # Проверяем, существует ли запись с данным chat_id_temp
    cursor.execute("SELECT * FROM users WHERE phone_number = %s OR chat_id_temp = %s", (number, chat_id))
    existing_user = cursor.fetchone()
    

    if existing_user:
        if existing_user[5] == message.from_user.id or existing_user[-1] == number:
            await message.answer(f'Добро пожаловать {existing_user[1]}!')
            if existing_user[3]:
                await message.answer(f"\nПродолжим. Выберите один из пунктов меню: ",
                                    reply_markup=kb.drivers, parse_mode='HTML')
            else:
                await message.answer(f"\nПродолжим. Выберите один из пунктов меню: ",
                                    reply_markup=kb.rentors, parse_mode='HTML')
    else:
        await message.answer(
                f'Добро пожаловать {message.from_user.first_name}, пожалуйста, выберите: <b>"Арендатор"</b> или '
                f'<b>"Водитель"</b>',
                reply_markup=kb.main, parse_mode="HTML")


@router.message(Command("help"))
async def help(message: Message):
    await message.answer('Чтобы получить оперативную помощь, напишите нам в личные сообщения: ',
                         reply_markup=kb.socials)


@router.message(Command("НАЗАД"))
@router.message(F.text == 'Вернуться в главное меню')
async def cancel_func(message: Message, state: FSMContext):
    cursor.execute('DELETE FROM users WHERE chat_id_temp = %s', (str(message.from_user.id), ))
    conn.commit()
    await state.clear()
    await message.answer(f'Вы вернулись к начальному шагу. Пожалуйста, предоставьте ваш номер телефона:',
                         reply_markup=kb.share_keyboard)


@router.message(F.text == 'Водитель')
async def driver(message: Message, state: FSMContext):
    await message.answer("Введите, пожалуйста, паспортные данные без пробелов: ", reply_markup=kb.back)
    await state.set_state(Driver.passport_finished)


@router.message(Driver.passport_finished)
async def passport_check(message: Message, state: FSMContext):
    user_input = message.text

    flag = 0
    for person in db.drivers:
        if person['passport_id'] == user_input:
            current_time = datetime.now()
            cursor.execute("INSERT INTO users (full_name, passport_number, user_type, event_time, chat_id_temp, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                str(message.from_user.first_name + ' ' + message.from_user.last_name), 
                                [str(user_input)],
                                True,
                                current_time, 
                                message.from_user.id,
                                number
                            )
                           )
            conn.commit()
            await message.answer(f"Паспортные данные верны. Добро пожаловать {person['FULL_NAME']}. "f"\nПродолжим. Выберите один из пунктов меню: ",
                                    reply_markup=kb.drivers, parse_mode='HTML')
            
            await state.update_data(found_person=person)
            await state.set_state(Driver.driver_data)
            flag = 1
    if flag == 0:
        await message.reply("Паспорта нет в базе данных. Попробуйте еще раз. \n\n При возникновении вопросов, нажмите /help")
        return
            



@router.message(F.text == 'Данные о заявке')
async def drivers_info(message: Message, state: FSMContext):
    data = await state.get_data()
    found_person = data.get('found_person')

    print('дата = ', data)

    if found_person:

        current_time = datetime.now()
        random_time_delta = timedelta(days=random.randint(1, 30),
                                      hours=random.randint(0, 23),
                                      minutes=random.randint(0, 59)
                                      )

        random_past_time = current_time - random_time_delta

        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        random_past_time_str = random_past_time.strftime("%Y-%m-%d %H:%M:%S")

        await message.answer(f"Информация о человеке:\n"
                             f"Ключ заявки: {found_person['ISSUE_KEY']}\n"
                             f"Полное имя: {found_person['FULL_NAME']}\n"
                             f"Номер автомобиля: {found_person['VEHICLE_PLATE']}\n"
                             f"Тип автомобиля: {found_person['VEHICLE_TYPE']}\n"
                             f"Состояние разрешения: {found_person['PERMIT_STATE']}\n"
                             f"Время нахождения в сети: C {random_past_time_str} до {current_time_str}")

    else:
        await message.answer('Информация о человеке не найдена.')


@router.message(F.text == 'Кол-во машин на территории')
async def car_amount(message: Message):
    car_am = random.randint(10, 50)
    await message.answer(f'Количество машин на территории: {car_am}')


@router.message(F.text == 'Кол-во машин в очереди')
async def car_amount(message: Message):
    car_am = random.randint(10, 50)
    await message.answer(f'Количество машин в очереди: {car_am}')
