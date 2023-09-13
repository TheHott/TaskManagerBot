from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from entity.models import Task
from entity.statuses import TaskStatus
from entity.callback_data import TaskIdCallbackData


def create_inline_for_actions(task: Task = None):
    builder = InlineKeyboardBuilder()

    if task.status == TaskStatus.COMPLETED.value:
        complete_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
    else:
        complete_btn = InlineKeyboardButton(text=Task.TASK_COMPLETE_ICON + " Выполнено",
                                            callback_data=TaskIdCallbackData(data="task_complete",
                                                                             task_id=task.id).pack())
    if task.status == TaskStatus.ACTIVE.value:
        not_complete_btn = InlineKeyboardButton(text=" ",
                                                callback_data="no_action")
    else:
        not_complete_btn = InlineKeyboardButton(text=Task.TASK_ACTIVE_ICON + " Не выполнено",
                                                callback_data=TaskIdCallbackData(data="task_not_complete",
                                                                                 task_id=task.id).pack())
    if task.status == TaskStatus.DRAFT.value:
        draft_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
    else:
        draft_btn = InlineKeyboardButton(text=Task.TASK_DRAFT_ICON + " В черновик",
                                         callback_data=TaskIdCallbackData(data="task_draft",
                                                                          task_id=task.id).pack())
    edit_btn = InlineKeyboardButton(text="✏ Редактировать",
                                    callback_data=TaskIdCallbackData(data="edit_task",
                                                                     task_id=task.id).pack())
    delete_btn = InlineKeyboardButton(text="🗑 Удалить",
                                      callback_data=TaskIdCallbackData(data="task_delete_confirm",
                                                                       task_id=task.id).pack())
    to_tasks_btn = InlineKeyboardButton(text="📝 К моим задачам",
                                        callback_data="my_tasks")
    to_drafts_btn = InlineKeyboardButton(text="✍ К черновикам",
                                         callback_data="drafts")
    to_menu_btn = InlineKeyboardButton(text="⬅ На главную", callback_data="main_menu")

    builder.row(complete_btn, not_complete_btn, draft_btn)
    builder.row(edit_btn, delete_btn)
    builder.row(InlineKeyboardButton(text=' ', callback_data='no_action'))
    builder.row(to_tasks_btn, to_drafts_btn)
    builder.row(to_menu_btn)

    return builder.as_markup()


def create_inline_for_confirming_deletion(task_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 Удалить",
                   callback_data=TaskIdCallbackData(data="delete_task",
                                                    task_id=task_id).pack())
    builder.button(text="⬅ Отменить", callback_data="delete_message")

    return builder.as_markup()
