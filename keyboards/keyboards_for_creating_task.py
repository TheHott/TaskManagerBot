from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_for_cancelling():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Отмена", callback_data="cancel_create_task")
    # ➕✍️⏱📅📆📝✉️❌⛔️⭕️❗️❕‼️🕒🔔🔕

    return builder.as_markup()


def create_inline_for_closing():
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Закрыть", callback_data="close_create_task")

    return builder.as_markup()
