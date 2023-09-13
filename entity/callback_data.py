from aiogram.filters.callback_data import CallbackData


class PageCallbackData(CallbackData, prefix='page_callback'):
    data: str
    page: int


class TaskIdCallbackData(CallbackData, prefix='task_id_callback'):
    data: str
    task_id: int


class PrefixCallbackData(CallbackData, prefix='prefix_callback'):
    data: str
    prefix: str
