import asyncio
import locale

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from entity import models
from handlers import menu, commands, create_task, drafts, etc, my_tasks, task, edit_task


async def main():
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    tg_token = config.get_telegram_token()

    bot = Bot(tg_token, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(menu.router, commands.router, create_task.router,
                       drafts.router, etc.router, my_tasks.router, task.router,
                       edit_task.router)

    model_list = [models.User, models.Role, models.Task]
    models.database.create_tables(model_list)

    await dp.start_polling(bot)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    asyncio.run(main())
