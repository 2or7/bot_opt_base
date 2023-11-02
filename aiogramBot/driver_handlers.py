from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import random
from datetime import datetime, timedelta

import keyboards as kb
import psycopg2

conn = psycopg2.connect(dbname='opt_base', user='postgres', password='postgres', host='127.0.0.1')

cursor = conn.cursor()

router = Router()

class Form_for_auth(StatesGroup):
    login_process = State()
    password_process = State()
    auth_finished = State()

class Driver(StatesGroup):
    GET_PASSPORT = State()
    driver_data = State()


@router.message(Command("start", ignore_case=True))
async def cmd_start(message: Message):
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
    cursor.execute("SELECT * FROM drivers WHERE drivers_phone = %s OR chat_id = %s", (number, chat_id))
    drivers_info = cursor.fetchone()
    

    cursor.execute("SELECT * FROM rentors_employees WHERE phone_number = %s OR chat_id = %s", (number, chat_id))
    rentors_info = cursor.fetchone()
    # if password == rentors_info[-1]:
    #     cursor.execute("UPDATE rentors_employees SET chat_id = %s WHERE phone_number = %s", (str(message.from_user.id), dh.number))
    #     conn.commit()
    #     await message.answer(f'Вход выполнен. {rentors_info[3]} {rentors_info[4]}', reply_markup=kb.rentors)
    #     await state.set_state(Form_for_auth.auth_finished)
    # else:
    #     await message.reply("Неверный пароль! Поробуйте ещё раз. \n\n При возникновении вопросов, нажмите /help", reply_markup=kb.back)
    #     return
    if drivers_info:
        if drivers_info[-1] == message.from_user.id or drivers_info[-2] == number:
            await message.answer(f'Добро пожаловать {drivers_info[1]} {drivers_info[2]} \nВыберите один из пунктов меню: ', reply_markup=kb.drivers, parse_mode='HTML')
        else:
            await message.answer('Добро пожаловать, введите ваши паспортные данные: ')
            await state.set_state(Driver.GET_PASSPORT)
            
    elif rentors_info:
        if rentors_info[-1] == message.from_user.id or rentors_info[2] == number:
            await message.answer(f'Введите логин', reply_markup=kb.back)
            await state.set_state(Form_for_auth.login_process)
        else:
            await message.answer('Извините, вас нет в базе арендаторов.', reply_markup=kb.socials_kb)
    else:
        await message.answer('Вас нет в базе данных арендаторов и водителей. Скорее всего, вы оставляли заявку. Пожалуйста, введите свой паспорт: ')    
        await state.set_state(Driver.GET_PASSPORT)
    
@router.message(Command("help"))
async def help(message: Message):
    await message.answer('Чтобы получить оперативную помощь, напишите нам в личные сообщения: ',
                         reply_markup=kb.socials)



@router.message(Command("НАЗАД"))
@router.message(F.text == 'Вернуться в главное меню')
async def cancel_func(message: Message, state: FSMContext):
    await message.answer(f'Вы вернулись к начальному шагу. Пожалуйста, предоставьте ваш номер телефона:',
                         reply_markup=kb.share_keyboard)


# @router.message(F.text == 'Водитель')
# async def driver(message: Message, state: FSMContext):
#     await message.answer("Введите, пожалуйста, паспортные данные без пробелов: ", reply_markup=kb.back)
#     await state.set_state(Driver.passport_finished)


@router.message(Driver.GET_PASSPORT)
async def passport_check(message: Message, state: FSMContext):
    user_input = message.text

    cursor.execute('SELECT * FROM applications WHERE driver_passport = %s', (user_input, ))
    driver_app = cursor.fetchone()
    if driver_app != None and driver_app[-3] == user_input:
        cursor.execute('INSERT INTO drivers (surname, name, patronymic, passport_number, drivers_license, drivers_phone, chat_id) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                       (
                            driver_app[4],
                            driver_app[5],
                            driver_app[6],
                            driver_app[7],
                            driver_app[8],
                            number,
                            message.from_user.id
                       )
                      )
        conn.commit()
        await message.answer(f"Паспортные данные верны. Добро пожаловать {driver_app[4]} {driver_app[5]} {driver_app[6]}. "f"\nПродолжим. Выберите один из пунктов меню: ",
                                reply_markup=kb.drivers, parse_mode='HTML')
        
        await state.update_data(found_person=driver_app)
        await state.set_state(Driver.driver_data)
    else:
        await message.reply("Паспорта нет в базе данных. Попробуйте еще раз. \n\n При возникновении вопросов, нажмите /help")
        return
            



@router.message(F.text == 'Данные о заявке')
async def drivers_info(message: Message, state: FSMContext):

    data = await state.get_data()
    driver_app = data.get('found_person')

    current_time = datetime.now()
    random_time_delta = timedelta(days=random.randint(1, 30),
                                    hours=random.randint(0, 23),
                                    minutes=random.randint(0, 59)
                                    )

    random_past_time = current_time - random_time_delta

    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    random_past_time_str = random_past_time.strftime("%Y-%m-%d %H:%M:%S")

    await message.answer(f"Информация о человеке:\n"
                            f"Ключ заявки: {driver_app[-1]}\n"
                            f"Полное имя: {driver_app[4] + ' ' + driver_app[5] + ' ' + driver_app[6]}\n"
                            f"Номер автомобиля: {driver_app[2]}\n"
                            f"Тип автомобиля: {driver_app[3]}\n"
                            f"Состояние разрешения: None \n"
                            f"Время нахождения в сети: C {random_past_time_str} до {current_time_str}")




@router.message(F.text == 'Кол-во машин на территории')
async def car_amount(message: Message):
    car_am = random.randint(10, 50)
    await message.answer(f'Количество машин на территории: {car_am}')


@router.message(F.text == 'Кол-во машин в очереди')
async def car_amount(message: Message):
    car_am = random.randint(10, 50)
    await message.answer(f'Количество машин в очереди: {car_am}')
