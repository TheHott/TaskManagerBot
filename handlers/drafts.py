from aiogram import Router, F
from aiogram.types import CallbackQuery

from entity.statuses import TaskStatus
from handlers.my_tasks import show_tasks_by_statuses

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
