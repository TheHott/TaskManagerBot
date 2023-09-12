from aiogram import Router, F
from aiogram.types import CallbackQuery

from entity.models import User, Task
from entity.statuses import TaskStatus
from handlers.menu import main_menu
from keyboards import keyboards_for_my_tasks

router = Router()


@router.callback_query(F.data.startswith('my_tasks_page#'))
async def my_tasks_page(call: CallbackQuery) -> None:
    page = int(call.data.split('#')[1])
    await my_tasks(call, page)


@router.callback_query(F.data == 'my_tasks')
async def my_tasks(call: CallbackQuery, page: int = 1) -> None:
    await call.answer()
    await show_tasks_by_statuses(call=call, prefix='my_tasks', header='📝 Мои задачи',
                                 no_value_text='📝 У вас нет задач!',
                                 statuses=[TaskStatus.COMPLETED, TaskStatus.ACTIVE], page=page)


# @router.callback_query(F.data == 'enter_page_number')
# todo


async def show_tasks_by_statuses(call: CallbackQuery, prefix='my_tasks', header='Мои задачи',
                                 no_value_text='У вас нет задач!', statuses=None, page: int = 1):
    if len(statuses) == 0 or statuses is None:
        task_list = []
    else:
        statuses = [status.value for status in statuses]
        user = User.get(User.telegram_id == call.from_user.id)
        task_list = Task \
            .select() \
            .where(Task.user_id == user.id and Task.status << statuses) \
            .order_by(Task.date)

    if len(task_list) == 0:
        await call.message.edit_text(no_value_text)
        await main_menu(call.message)
    else:
        await call.message.edit_text(header,
                                     reply_markup=keyboards_for_my_tasks.show_my_tasks(task_list,
                                                                                       prefix=prefix,
                                                                                       page=page))
