import copy

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from entity.models import Task
from entity.statuses import TaskStatus
from handlers.drafts import drafts
from handlers.my_tasks import my_tasks
from keyboards import keyboards_for_task

router = Router()


@router.callback_query(F.data.startswith('show_task#'))
async def show_task(call: CallbackQuery) -> None:
    task_id = call.data.split('#')[1]
    task = Task.get_by_id(task_id)
    await call.message.edit_text(task.get_task_as_message(),
                                 reply_markup=keyboards_for_task.create_inline_for_actions(task))


@router.callback_query(F.data.startswith('task_complete#'))
async def complete_task(call: CallbackQuery) -> None:
    task_id = call.data.split('#')[1]
    task = Task.get_by_id(task_id)
    task.status = TaskStatus.COMPLETED.value
    task.save()

    await show_task(call)


@router.callback_query(F.data.startswith('task_not_complete#'))
async def task_not_complete(call: CallbackQuery) -> None:
    task_id = call.data.split('#')[1]
    task = Task.get_by_id(task_id)
    task.status = TaskStatus.ACTIVE.value
    task.save()

    await show_task(call)


@router.callback_query(F.data.startswith('task_draft#'))
async def task_draft(call: CallbackQuery) -> None:
    task_id = call.data.split('#')[1]
    task = Task.get_by_id(task_id)
    task.status = TaskStatus.DRAFT.value
    task.save()

    await show_task(call)


@router.callback_query(F.data.startswith('task_delete_confirm#'))
async def confirm_task_delete(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    task_id = call.data.split('#')[1]
    await state.update_data(task_message=call.message)

    await call.message.answer("Вы уверены, что хотите удалить эту задачу?",
                              reply_markup=keyboards_for_task.create_inline_for_confirming_deletion(task_id))


@router.callback_query(F.data.startswith('delete_task#'))
async def delete_task(call: CallbackQuery, state: FSMContext) -> None:
    task_id = call.data.split('#')[1]
    task = Task.get_by_id(task_id)
    previous_status = copy.copy(task.status)
    task.status = TaskStatus.DELETED.value
    task.save()

    state_data = await state.get_data()
    await state_data['task_message'].delete()

    if previous_status == TaskStatus.DRAFT.value:
        await drafts(call)
    else:
        await my_tasks(call)
