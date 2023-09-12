from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from entity.models import Task
from entity.user_state import EditTaskState
from keyboards import keyboards_for_editing_task

router = Router()


@router.callback_query(F.data.startswith('edit_task#'))
async def edit_task(call: CallbackQuery) -> None:
    await call.answer()
    task_id = call.data.split('#')[1]
    task = Task.get_by_id(task_id)

    await call.message.edit_text(task.get_task_as_message(),
                                 reply_markup=keyboards_for_editing_task.create_inline_for_editing(task))


@router.callback_query(F.data.startswith('enter_new_task_name#'))
async def enter_new_task_name(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await state.set_state(EditTaskState.entering_new_name)
    task_id = call.data.split('#')[1]
    sent_message = await call.message.answer(
        '<b>Введите название задачи</b>',
        reply_markup=keyboards_for_editing_task.create_inline_for_deleting_message())

    await state.update_data(task_id=task_id, preview_message_call=call, enter_name_message=sent_message)


@router.message(EditTaskState.entering_new_name)
async def edit_task_name(message: Message, state: FSMContext):
    state_data = await state.get_data()
    task_id = state_data['task_id']
    task = Task.get_by_id(task_id)
    task.text = message.text
    task.save()

    await state_data['enter_name_message'].delete()

    await message.delete()
    await edit_task(state_data['preview_message_call'])
    await state.clear()


@router.callback_query(F.data.startswith('enter_new_task_description#'))
async def enter_new_task_description(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await state.set_state(EditTaskState.entering_new_description)
    task_id = call.data.split('#')[1]
    sent_message = await call.message.answer(
        '<b>Введите описание задачи</b>',
        reply_markup=keyboards_for_editing_task.create_inline_for_deleting_message())

    await state.update_data(task_id=task_id, preview_message_call=call, enter_description_message=sent_message)


@router.message(EditTaskState.entering_new_description)
async def edit_task_description(message: Message, state: FSMContext):
    state_data = await state.get_data()
    task_id = state_data['task_id']
    task = Task.get_by_id(task_id)
    task.description = message.text
    task.save()

    await state_data['enter_description_message'].delete()

    await message.delete()
    await edit_task(state_data['preview_message_call'])
    await state.clear()


@router.callback_query(F.data.startswith('enter_new_task_date#'))
async def enter_new_task_date(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await state.set_state(EditTaskState.entering_new_date)
    task_id = call.data.split('#')[1]
    sent_message = await call.message.answer(
        '<b>Введите дату задачи</b>',
        reply_markup=keyboards_for_editing_task.create_inline_for_deleting_message())

    await state.update_data(task_id=task_id, preview_message_call=call, enter_date_message=sent_message)


@router.message(EditTaskState.entering_new_date)
async def edit_task_date(message: Message, state: FSMContext):
    state_data = await state.get_data()
    task_id = state_data['task_id']
    task = Task.get_by_id(task_id)
    task.date = message.text
    task.save()

    await state_data['enter_date_message'].delete()

    await message.delete()
    await edit_task(state_data['preview_message_call'])
    await state.clear()


@router.callback_query(F.data.startswith('enter_new_task_time#'))
async def enter_new_task_time(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await state.set_state(EditTaskState.entering_new_time)
    task_id = call.data.split('#')[1]
    sent_message = await call.message.answer(
        '<b>Введите время задачи</b>',
        reply_markup=keyboards_for_editing_task.create_inline_for_deleting_message())

    await state.update_data(task_id=task_id, preview_message_call=call, enter_time_message=sent_message)


@router.message(EditTaskState.entering_new_time)
async def edit_task_time(message: Message, state: FSMContext):
    state_data = await state.get_data()
    task_id = state_data['task_id']
    task = Task.get_by_id(task_id)
    task.time = message.text
    task.save()

    await state_data['enter_time_message'].delete()

    await message.delete()
    await edit_task(state_data['preview_message_call'])
    await state.clear()
