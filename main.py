import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

import config

# from aiogram.fsm.storage.redis import RedisStorage

TG_TOKEN = config.get_telegram_token()
bot = Bot(TG_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def start_bot():
    await dp.start_polling(bot)


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer("Привет!")


@dp.message()
async def echo_message(message: Message):
    await message.answer(message.text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(start_bot())
