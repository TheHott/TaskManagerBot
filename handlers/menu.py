from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import keyboards_for_menu

router = Router()


@router.callback_query(F.data == 'main_menu')
async def go_to_main_menu_from_callback(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text("Добро пожаловать в менеджер задач!",
                                 reply_markup=keyboards_for_menu.create_inline_menu())


# @router.message()
# async def unknown_command(message: Message):
#     await main_menu(message)


async def main_menu(message: Message):
    await message.answer("Добро пожаловать в менеджер задач!",
                         reply_markup=keyboards_for_menu.create_inline_menu())
