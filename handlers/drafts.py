from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from entity.statuses import TaskStatus
from entity.user_state import TaskListState
from handlers.my_tasks import show_tasks_by_statuses, my_tasks
from keyboards import keyboards_for_other

router = Router()


@router.callback_query(F.data.startswith('drafts_page#'))
async def drafts_page(call: CallbackQuery) -> None:
    page = int(call.data.split('#')[1])
    await drafts(call, page)


@router.callback_query(F.data == 'drafts')
async def drafts(call: CallbackQuery, page: int = 1) -> None:
    await call.answer()
    await show_tasks_by_statuses(call=call, prefix='drafts', header='✍ Мои черновики',
                                 no_value_text='✍ У вас нет черновиков!',
                                 statuses=[TaskStatus.DRAFT], page=page)


@router.callback_query(F.data.startswith('enter_page_number#'))
async def enter_page_number(call: CallbackQuery, state: FSMContext):
    await call.answer()
    prefix = call.data.split('#')[1]  # my_tasks или drafts
    await state.set_state(TaskListState.entering_page_number)

    message_to_delete = await call.message.answer(
        'Введите номер страницы',
        reply_markup=keyboards_for_other.create_inline_for_delete_message_and_finish_state())

    await state.update_data(prefix=prefix, message_to_delete=message_to_delete, initial_call=call)


@router.message(TaskListState.entering_page_number)
async def user_entered_page_number(message: Message, state: FSMContext):
    state_data = await state.get_data()

    message_to_delete = state_data['message_to_delete']

    try:
        page = int(message.text)
    except ValueError:
        await message.delete()
        if message_to_delete.text != '⚠️ Пожалуйста, введите НОМЕР страницы!':
            await state.update_data(
                message_to_delete=await message_to_delete.edit_text(
                    '⚠️ Пожалуйста, введите НОМЕР страницы!',
                    reply_markup=keyboards_for_other.create_inline_for_delete_message_and_finish_state()))
        return

    await message.delete()
    await message_to_delete.delete()

    prefix = state_data['prefix']
    call = state_data['initial_call']

    if prefix == 'my_tasks':
        await my_tasks(call, page)
    elif prefix == 'drafts':
        await drafts(call, page)
