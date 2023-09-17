from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import asyncio

import keyboards as kb

bot = Bot(token='6354167807:AAGnX8EmmFOPc3tgwZIWg6xqm64prvC3y6k')
dp = Dispatcher()


@dp.message(F.text == "/start")
async def cmd_start(messege: Message):
    await messege.answer(f'Добро пожаловать {messege.from_user.first_name}, пожалуйста, выберите "Арендатор" или "Водитель"',
                         reply_markup=kb.main)


@dp.message(F.text == '/my_id')
async def user_id(message: Message):
    await message.answer(f"Ваш id: {message.from_user.id}")
    await message.answer(f"Вашe Имя: {message.from_user.first_name}")


@dp.message(F.text == 'Контакты')
async def contacts(message: Message):
    await message.answer('Список наших контактов:', reply_markup=kb.socials)


@dp.message(F.text == 'Помощь')
async def help(message: Message):
    await message.answer('Чтобы получить оперативную помощь, напишите нам в личные сообщения: ', reply_markup=kb.socials)


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())




