from aiogram import Bot, Dispatcher
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from driver_handlers import router
from rent_handlers import rt_router


async def main():
    bot = Bot(token='6354167807:AAGnX8EmmFOPc3tgwZIWg6xqm64prvC3y6k')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.include_router(rt_router)
    await dp.start_polling(bot)
  


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')




