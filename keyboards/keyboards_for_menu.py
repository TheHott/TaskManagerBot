from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_menu():
    builder = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text="📝 Мои задачи", callback_data="my_tasks")
    btn2 = InlineKeyboardButton(text="✍ Черновики", callback_data="drafts")
    btn3 = InlineKeyboardButton(text="➕ Создать задачу", callback_data="create_task")
    # builder.row(btn1, btn2, btn3)
    builder.row(btn1)
    builder.row(btn2)
    builder.row(btn3)

    return builder.as_markup()
