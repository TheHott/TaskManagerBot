from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from entity.models import Task, User
from entity.statuses import TaskStatus
from entity.user_state import CreateTaskState
from handlers.menu import main_menu
from keyboards import keyboards_for_creating_task, keyboards_for_task

router = Router()


@router.callback_query(F.data == 'create_task')
async def create_task(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.delete()
    preview_message = await call.message.answer(Task().get_task_as_message())
    await call.message.answer("Введите название задачи",
                              reply_markup=keyboards_for_creating_task.create_inline_for_cancelling())
    await state.update_data(preview_message=preview_message)
    await state.set_state(CreateTaskState.create_task_entering_text)


@router.message(CreateTaskState.create_task_entering_text)
async def create_task_enter_description(message: Message, state: FSMContext) -> None:
    current_user = User.get_or_none(User.telegram_id == message.from_user.id)
    task = Task.create(text=message.text, user_id=current_user.id)
    state_data = await state.get_data()

    await state_data['preview_message'].delete()
    preview_message = await message.answer(task.get_task_as_message())
    await message.answer("Введите описание задачи",
                         reply_markup=keyboards_for_creating_task.create_inline_for_closing())

    await state.set_state(CreateTaskState.create_task_entering_description)
    await state.update_data(task_id=task.id, preview_message=preview_message)


@router.message(CreateTaskState.create_task_entering_description)
async def create_task_enter_description(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    task = Task.get_or_none(Task.id == state_data['task_id'])
    task.description = message.text
    task.save()

    await state_data['preview_message'].delete()
    preview_message = await message.answer(task.get_task_as_message())
    await message.answer("Введите дату задачи",
                         reply_markup=keyboards_for_creating_task.create_inline_for_closing())

    await state.set_state(CreateTaskState.create_task_entering_date)
    await state.update_data(preview_message=preview_message)


@router.message(CreateTaskState.create_task_entering_date)
async def create_task_enter_date(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    task = Task.get_or_none(Task.id == state_data['task_id'])
    task.date = message.text
    task.save()

    await state_data['preview_message'].delete()
    preview_message = await message.answer(task.get_task_as_message())
    await message.answer("Введите время задачи",
                         reply_markup=keyboards_for_creating_task.create_inline_for_closing())

    await state.set_state(CreateTaskState.create_task_entering_time)
    await state.update_data(preview_message=preview_message)


@router.message(CreateTaskState.create_task_entering_time)
async def create_task_enter_time(message: Message, state: FSMContext) -> None:
    state_data = await state.get_data()
    task = Task.get_or_none(Task.id == state_data['task_id'])
    task.time = message.text
    task.status = TaskStatus.ACTIVE.value
    task.save()

    await state_data['preview_message'].delete()
    await message.answer(task.get_task_as_message() + '\n',
                         reply_markup=keyboards_for_task.create_inline_for_actions(task))


@router.callback_query(F.data == 'cancel_create_task')
async def cancel_create_task(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.delete()
    state_data = await state.get_data()
    await state_data['preview_message'].delete()
    await main_menu(call.message)


@router.callback_query(F.data == 'close_create_task')
async def cancel_create_task(call: CallbackQuery, state: FSMContext) -> None:
    await call.answer()
    await call.message.delete()
    state_data = await state.get_data()
    await state_data['preview_message'].delete()
    await call.message.answer("Ваша задача была сохранена как черновик")
    await main_menu(call.message)
