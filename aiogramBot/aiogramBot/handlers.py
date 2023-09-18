from aiogram import Router, F
from aiogram.fsm import state
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Filter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import random
from datetime import datetime, timedelta

import keyboards as kb
import database as db

router = Router()


class Form(StatesGroup):
    passport_process = State()
    passport_finished = State()


class Form_for_auth(StatesGroup):
    login_process = State()
    password_process = State()
    auth_finished = State()


class Form_for_search_car(StatesGroup):
    plate_process = State()


@router.message(Command("start"))
async def cmd_start(messege: Message):
    await messege.answer(
        f'Добро пожаловать {messege.from_user.first_name}, пожалуйста, выберите: <b>"Арендатор"</b> или <b>"Водитель"</b>',
        reply_markup=kb.main, parse_mode="HTML")


#-----------------------------------------------------------------------------------------------------#


@router.message(F.text == 'Арендатор')
async def message_to_input_login(message: Message, state: FSMContext):
    await message.answer(f'Введите логин')
    await state.set_state(Form_for_auth.login_process)


@router.message(Form_for_auth.login_process)
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
        await message.reply("Пользователь не найден! Поробуйте ещё раз.")
        return


@router.message(Form_for_auth.password_process)
async def input_password(message: Message, state: FSMContext):
    password = message.text
    flag_password = 0
    if password == db.rentors[rentor_id]["PASSWORD"]:
        await message.answer(f'Вход выполнен', reply_markup=kb.rentors)
        flag_password = 1
        await state.set_state(Form_for_auth.auth_finished)
    if flag_password != 1:
        await message.reply("Неверный пароль! Поробуйте ещё раз.")
        return


# @router.message(Form.auth_finished)
# async def show_keyboard(message: Message, state: FSMContext):
#     await message.answer('Выберите действие, которое хотите выполнить: ', reply_markup=kb.rentors)


@router.message(F.text == 'Общее количество заявок')
async def info(message: Message):
    await message.answer(f'Общее количество заявок: {random.randint(10, 50)}')


@router.message(F.text == 'Количество выданных пропусков')
async def info(message: Message):
    await message.answer(f'Количество выданных пропусков: {random.randint(10, 50)}')


@router.message(F.text == 'Количесвто автомобилей на территории')
async def info(message: Message):
    await message.answer(f'Количесвто автомобилей на территории: {random.randint(10, 50)}')


@router.message(F.text == 'Количесвто свободных мест')
async def info(message: Message):
    await message.answer(f'Количесвто свободных мест: {random.randint(10, 50)}')


@router.message(F.text == 'Количество завершённых заявок')
async def info(message: Message):
    await message.answer(f'Количество завершённых заявок: {random.randint(10, 50)}')


@router.message(F.text == 'Детальные данные по конкретному автомобилю')
async def input_plate(message: Message, state: FSMContext):
    await message.answer(f'Введите госномер автомобиля')
    await state.set_state(Form_for_search_car.plate_process)


@router.message(Form_for_search_car.plate_process)
async def detaile_info(message: Message, state: FSMContext):
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
        await message.reply("Автомобиля нет в базе данных. Попробуйте еще раз. ")
        return


#-----------------------------------------------------------------------------------------------------#

@router.message(F.text == 'Водитель')
async def driver(message: Message, state: FSMContext):
    await message.answer("Введите, пожалуйста, паспортные данные без пробелов: ")
    await state.set_state(Form.passport_process)


@router.message(Form.passport_process)
async def passport_finished(message: Message, state: FSMContext):
    user_input = message.text
    flag = 0
    for person in db.drivers:
        if person['passport_id'] == user_input:
            await message.answer(f"Паспортные данные верны. Добро пожаловать {person['FULL_NAME']}. "
                                 f"\nПродолжим. Выберите один из пунктов меню: ",
                                 reply_markup=kb.drivers, parse_mode='HTML')
            await state.set_state(Form.passport_finished)
            await state.update_data(found_person=person)
            flag = 1
    if flag == 0:
        await message.reply("Паспорта нет в базе данных. Попробуйте еще раз. ")
        return


@router.message(F.text == 'Сведения о заявке')
async def drivers_info(message: Message, state: FSMContext):
    data = await state.get_data()
    found_person = data.get('found_person')

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


@router.message(F.text == 'Контакты')
async def contacts(message: Message):
    await message.answer('Список наших контактов:', reply_markup=kb.socials)


@router.message(F.text == 'Помощь')
async def help(message: Message):
    await message.answer('Чтобы получить оперативную помощь, напишите нам в личные сообщения: ',
                         reply_markup=kb.socials)
