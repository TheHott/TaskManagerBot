from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_for_delete_message_and_finish_state(button_text="⬅ Отменить"):
    builder = InlineKeyboardBuilder()
    builder.button(text=button_text, callback_data="delete_message_and_finish_state")

    return builder.as_markup()


def create_inline_for_delete_message(button_text="⬅ Отменить"):
    builder = InlineKeyboardBuilder()
    builder.button(text=button_text, callback_data="delete_message")

    return builder.as_markup()
