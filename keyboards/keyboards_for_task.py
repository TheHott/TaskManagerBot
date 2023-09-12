from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from entity.models import Task
from entity.statuses import TaskStatus


def create_inline_for_actions(task: Task = None):
    builder = InlineKeyboardBuilder()

    if task.status == TaskStatus.COMPLETED.value:
        complete_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
    else:
        complete_btn = InlineKeyboardButton(text=Task.TASK_COMPLETE_ICON + " Выполнено",
                                            callback_data="task_complete#" + str(task.id))
    if task.status == TaskStatus.ACTIVE.value:
        not_complete_btn = InlineKeyboardButton(text=" ",
                                                callback_data="no_action")
    else:
        not_complete_btn = InlineKeyboardButton(text=Task.TASK_ACTIVE_ICON + " Не выполнено",
                                                callback_data="task_not_complete#" + str(task.id))
    if task.status == TaskStatus.DRAFT.value:
        draft_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
    else:
        draft_btn = InlineKeyboardButton(text=Task.TASK_DRAFT_ICON + " В черновик",
                                         callback_data="task_draft#" + str(task.id))
    edit_btn = InlineKeyboardButton(text="✏ Редактировать", callback_data="edit_task#" + str(task.id))
    delete_btn = InlineKeyboardButton(text="🗑 Удалить", callback_data="task_delete_confirm#" + str(task.id))
    if task.status == TaskStatus.DRAFT.value:
        to_tasks_btn = InlineKeyboardButton(text="⬅ Назад в черновики", callback_data="drafts")
    else:
        to_tasks_btn = InlineKeyboardButton(text="⬅ Назад в мои задачи", callback_data="my_tasks")
    to_menu_btn = InlineKeyboardButton(text="⬅ На главную", callback_data="main_menu")

    builder.row(complete_btn, not_complete_btn, draft_btn)
    builder.row(edit_btn, delete_btn)
    builder.row(InlineKeyboardButton(text=' ', callback_data='no_action'))
    builder.row(to_tasks_btn)
    builder.row(to_menu_btn)

    return builder.as_markup()


def create_inline_for_confirming_deletion(task_id: str):
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 Удалить", callback_data="delete_task#" + task_id)
    builder.button(text="⬅ Отменить", callback_data="delete_message")

    return builder.as_markup()
