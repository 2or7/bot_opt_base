from aiogram import Bot, Dispatcher
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from driver_handlers import router, consume
from rent_handlers import rt_router



async def main():
    bot = Bot(token='6354167807:AAGnX8EmmFOPc3tgwZIWg6xqm64prvC3y6k')
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    dp.include_router(rt_router)
    consume_task = asyncio.create_task(consume())
    await dp.start_polling(bot)
    await consume_task
    


if __name__ == '__main__':
    asyncio.run(main())
