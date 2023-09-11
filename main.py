import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.fsm.storage.redis import RedisStorage

TG_TOKEN = '6518925746:AAH0rZpZXJ_a48h36Hj7gw6V2UA6eaBIJHM'
bot = Bot(TG_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def start_bot():
    await dp.start_polling(bot)


@dp.message()
async def echo_message(message: types.Message):
    await message.answer(message.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(start_bot())
