from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == 'no_action')
async def no_actions(call: CallbackQuery) -> None:
    await call.answer()


@router.callback_query(F.data == 'delete_message')
async def delete_message(call: CallbackQuery) -> None:
    await call.message.delete()


@router.callback_query(F.data == 'delete_message_and_finish_state')
async def delete_message_and_finish_state(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.delete()
    await state.clear()
