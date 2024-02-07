from aiogram import Router, F, types
import aio_pika
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot
import random
from datetime import datetime, timedelta
import json
import keyboards as kb
import psycopg2
import asyncio


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

async def connect_to_rabbitmq() -> str:
    connection = await aio_pika.connect_robust(
        host='81.94.159.234',
        login='opt_base',
        password='optbasebot',
        virtualhost='/'
    )
    return connection

@router.message(Command("start", ignore_case=True))
async def cmd_start(message: Message):
    await message.reply("Привет, чтобы отправить мне свой номер телефона, нажмите на кнопку ниже.",
                        reply_markup=kb.share_keyboard, parse_mode='HTML')



bot = Bot(token='6354167807:AAGnX8EmmFOPc3tgwZIWg6xqm64prvC3y6k')

async def consume():
    #try:
    print('[ ] Receiving queue...')
    # Подключение к RabbitMQ для второй очереди
    connection = await connect_to_rabbitmq()
    channel = await connection.channel()
    queue_name = 'receive_queue'
    # Подключение к второй очереди
    queue = await channel.declare_queue(queue_name)
    while True:
        try:
            message = await queue.get(timeout=2)
            if message:
                await process_message(message)
                
                await asyncio.sleep(3)
        except aio_pika.exceptions.QueueEmpty:
            await asyncio.sleep(3)



async def process_message(message: types.Message):
    body = message.body.decode()
    body_json = json.loads(body)
    print(f"Received message: {body}")
    await bot.send_message(chat_id=int(body_json["chat_id"]), text=body_json["text"], parse_mode='HTML')


@router.message(lambda message: message.contact is not None)
async def login(message: Message, state: FSMContext):
    temp = str(message.contact.phone_number)
    global number
    if '+' == temp[0]:
        number = temp[1:]
    else:
        number = temp

    print(number)
    chat_id = str(message.from_user.id)
    
   
    cursor.execute("SELECT * FROM drivers WHERE drivers_phone = %s OR chat_id = %s", (number, chat_id))
    drivers_info = cursor.fetchone()
    
    cursor.execute("SELECT * FROM rentors_employees WHERE phone_number = %s OR chat_id = %s", (number, chat_id))
    rentors_info = cursor.fetchone()
    if drivers_info:
        if drivers_info[-1] == message.from_user.id or drivers_info[-2] == number:
            await message.answer(f'Добро пожаловать {drivers_info[1]} {drivers_info[2]} \nВыберите один из пунктов меню: ', reply_markup=kb.drivers, parse_mode='HTML')
        else:
            await message.answer('Добро пожаловать, введите ваши паспортные данные: ')
            await state.set_state(Driver.GET_PASSPORT)
    elif rentors_info:
        if rentors_info[-3] != None:
            await message.answer(f'Вход выполнен. {rentors_info[3]} {rentors_info[4]}', reply_markup=kb.rentors)
            await state.set_state(Form_for_auth.auth_finished)
        elif rentors_info[-1] == message.from_user.id or rentors_info[2] == number:
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

        await state.update_data(passport_number=user_input)  # Store passport_number in the state
        await state.set_state(Driver.driver_data)
    else:
        await message.reply("Паспорта нет в базе данных. Попробуйте еще раз. \n\n При возникновении вопросов, нажмите /help")
        return
            



@router.message(F.text == 'Данные о заявке')
async def drivers_info(message: Message, state: FSMContext):
    state_data = await state.get_data()
    print('number= ', number)
    cursor.execute('SELECT * FROM applications JOIN drivers ON applications.driver_passport = drivers.passport_number WHERE drivers.drivers_phone = %s', (number, ))
    driver_app = cursor.fetchone()
    print(driver_app)

    current_time = datetime.now()
    random_time_delta = timedelta(days=random.randint(1, 30),
                                    hours=random.randint(0, 23),
                                    minutes=random.randint(0, 59)
                                    )

    random_past_time = current_time - random_time_delta

    current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    random_past_time_str = random_past_time.strftime("%Y-%m-%d %H:%M:%S")

    await message.answer(f"Информация о человеке:\n"
                            f"Ключ заявки: {driver_app[0]}\n"
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

