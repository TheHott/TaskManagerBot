from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from entity.statuses import TaskStatus


def create_inline_for_editing(task):
    builder = InlineKeyboardBuilder()
    name_btn = InlineKeyboardButton(text="ℹ Редактировать название",
                                    callback_data="enter_new_task_name#" + str(task.id))
    desc_btn = InlineKeyboardButton(text="📄 Редактировать описание",
                                    callback_data="enter_new_task_description#" + str(task.id))
    date_btn = InlineKeyboardButton(text="📅 Редактировать дату",
                                    callback_data="enter_new_task_date#" + str(task.id))
    time_btn = InlineKeyboardButton(text="⏱ Редактировать время",
                                    callback_data="enter_new_task_time#" + str(task.id))
    show_task_btn = InlineKeyboardButton(text="Назад к задаче",
                                         callback_data="show_task#" + str(task.id))

    if task.status == TaskStatus.DRAFT.value:
        back_to_tasks_btn = InlineKeyboardButton(text="Назад к черновикам", callback_data='drafts')
    else:
        back_to_tasks_btn = InlineKeyboardButton(text="Назад к моим задачам", callback_data='my_tasks')

    builder.row(name_btn)
    builder.row(desc_btn)
    builder.row(date_btn)
    builder.row(time_btn)
    builder.row(show_task_btn)
    builder.row(back_to_tasks_btn)

    return builder.as_markup()


def create_inline_for_deleting_message():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅ Отмена", callback_data="delete_message_and_finish_state")

    return builder.as_markup()

# def create_inline_for_cancelling():
#     builder = InlineKeyboardBuilder()
#     builder.button(text="⬅ Отмена", callback_data="cancel_create_task")
#     ➕✍️⏱📅📆📝✉️❌⛔️⭕️❗️❕‼️🕒🔔🔕
    #
    # return builder.as_markup()
#
#
# def create_inline_for_closing():
#     builder = InlineKeyboardBuilder()
#     builder.button(text="❌ Закрыть", callback_data="close_create_task")
#
#     return builder.as_markup()
