from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import random
from datetime import datetime, timedelta

import keyboards as kb
import database as db
import rent_handlers as rt

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


@router.message(rt.Form_for_auth.start_state, Command("start", ignore_case=True))
async def cmd_start(messege: Message):
    await messege.answer(
        f'Добро пожаловать {messege.from_user.first_name}, пожалуйста, выберите: <b>"Арендатор"</b> или <b>"Водитель"</b>',
        reply_markup=kb.main, parse_mode="HTML")


@router.message(Command("help"))
async def help(message: Message):
    await message.answer('Чтобы получить оперативную помощь, напишите нам в личные сообщения: ',
                         reply_markup=kb.socials)


@router.message(Command("cancel"))
async def cancel_func(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f'Вы вернулись к начальному выбору. Пожалуйста, выберите "Арендатор" или "Водитель":',
                         reply_markup=kb.main)


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
        await message.reply("Паспорта нет в базе данных. Попробуйте еще раз. \n\n При возникновении вопросов, нажмите /help")
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




