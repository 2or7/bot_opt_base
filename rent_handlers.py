from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from driver_handlers import cursor, conn
import random
from datetime import datetime
from aiogram import types
import keyboards as kb
import driver_handlers as dh
import aio_pika




rt_router = Router()

async def connect_to_rabbitmq():
    connection = await aio_pika.connect_robust(
        host='81.94.159.234',
        login='opt_base',
        password='optbasebot',
        virtualhost='/'
    )
    
    return connection


async def send_to_queue(event, chat_id, body):
    try:
        print('[ ] Sending queue...')
        # Подключение к RabbitMQ
        connection = await connect_to_rabbitmq()
        channel = await connection.channel()

        queue_name = 'send_queue'
        # Подключение к очереди
        queue = await channel.declare_queue(queue_name)

        message = {"event": event, "chatid": chat_id, "body": body}
        message_body = str(message)

        # Отправление сообщения в очередь
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=queue.name
        )

    except:
        # Закрытие соединения
        print('[x] Error detected!')
    finally:
        # Закрытие соединения
        print('[o] Closed successfully!')
        await connection.close()
        



class Form_for_auth(StatesGroup):
    login_process = State()
    password_process = State()
    auth_finished = State()


class Form_for_search_car(StatesGroup):
    plate_process = State()


@rt_router.message(lambda message: message.content_type not in ['text', 'contact'])
async def block_files(message: types.Message):
    try:
        
        cursor.execute("SELECT chat_id FROM rentors_employees WHERE phone_number = %s", (dh.number, ))
        rentors_info = cursor.fetchone()
        print(f'rentint ={rentors_info}')
        if rentors_info == (None,):
            await message.reply("Извините, но бот принимает файлы только от авторизованного арендатора.")
        else:
            file_name = message.document.file_name
            await message.reply("Файл успешно отправлен!")
            # Отправляем сообщение в очередь
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            await send_to_queue(event="document_received", chat_id=message.chat.id, body=f"File received: {file_name} at time: {current_time}")

    except:
        await message.reply("Перед отправкой файла, предоставьте номер телефона.", reply_markup=kb.share_keyboard)



@rt_router.message(Form_for_auth.login_process)
async def input_login(message: Message, state: FSMContext):
    login = message.text
    cursor.execute("SELECT * FROM rentors_employees WHERE phone_number = %s OR chat_id = %s", (dh.number, str(message.from_user.id)))
    rentors_info = cursor.fetchone()
    if login == rentors_info[-2]:
        await message.answer(f'Пользователь найден! Введите пароль.', reply_markup=kb.back)
        await state.update_data(found_person=rentors_info)
        await state.set_state(Form_for_auth.password_process)
    else:
        await message.reply("Пользователь не найден! Поробуйте ещё раз.\n\n При возникновении вопросов, нажмите /help", reply_markup=kb.back)
        return


@rt_router.message(Form_for_auth.password_process)
async def input_password(message: Message, state: FSMContext):
    data = await state.get_data()
    rentors_info = data.get('found_person')
    password = message.text
    if password == rentors_info[-1]:
        cursor.execute("UPDATE rentors_employees SET chat_id = %s WHERE phone_number = %s", (str(message.from_user.id), dh.number))
        conn.commit()
        
        
        
        await message.answer(f'Вход выполнен. {rentors_info[3]} {rentors_info[4]}', reply_markup=kb.rentors)
        
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
    print(plate)
    flag_plate = 0
    cursor.execute('SELECT * FROM applications WHERE car_number = %s', (plate, ))
    driver_app = cursor.fetchone()
    if driver_app != None:
        await message.answer(f"Информация о человеке:\n"
                                f"Полное имя: {driver_app[4] + ' ' + driver_app[5] + ' ' + driver_app[6]}\n"
                                f"Номер автомобиля: {driver_app[2]}\n"
                                f"Тип автомобиля: {driver_app[3]}\n"
                                f"Состояние разрешения: Processing...")
    else:
        await message.reply("Автомобиля нет в базе данных. Попробуйте еще раз. \n\n При возникновении вопросов, нажмите /help")
        return
