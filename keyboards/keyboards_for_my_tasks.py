import math

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from entity.callback_data import PrefixCallbackData, TaskIdCallbackData, PageCallbackData

PAGE_SIZE = 10


def show_my_tasks(task_list, prefix='', page=1):
    builder = InlineKeyboardBuilder()
    amount_of_tasks = len(task_list)
    amount_of_pages = math.ceil(amount_of_tasks / PAGE_SIZE)

    if page > amount_of_pages:
        page = amount_of_pages
    elif page < 1:
        page = 1

    first_item_index = PAGE_SIZE * (page - 1)
    last_item_index = PAGE_SIZE * page
    if last_item_index > amount_of_tasks:
        last_item_index = amount_of_tasks

    for i in range(first_item_index, last_item_index):
        task = task_list[i]
        builder.row(InlineKeyboardButton(text=task.as_short_str(),
                                         callback_data=TaskIdCallbackData(data="show_task",
                                                                          task_id=task.get_id()).pack()))
    if amount_of_pages > 1:
        if page == 1:
            first_page_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
            previous_page_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
        else:
            first_page_btn = InlineKeyboardButton(text="⏮",
                                                  callback_data=PageCallbackData(data=prefix + "_page",
                                                                                 page=1).pack())
            previous_page_btn = InlineKeyboardButton(text="◀️",
                                                     callback_data=PageCallbackData(data=prefix + "_page",
                                                                                    page=page - 1).pack())
        page_count_btn = InlineKeyboardButton(text=str(page) + '/' + str(amount_of_pages),
                                              callback_data=PrefixCallbackData(data="enter_page_number",
                                                                               prefix=prefix).pack())
        if page == amount_of_pages:
            next_page_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
            last_page_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
        else:
            next_page_btn = InlineKeyboardButton(text="▶️",
                                                 callback_data=PageCallbackData(data=prefix + "_page",
                                                                                page=page + 1).pack())
            last_page_btn = InlineKeyboardButton(text="⏭",
                                                 callback_data=PageCallbackData(data=prefix + "_page",
                                                                                page=amount_of_pages).pack())
        builder.row(first_page_btn, previous_page_btn, page_count_btn, next_page_btn, last_page_btn)

    main_menu_btn = InlineKeyboardButton(text="На главную", callback_data="main_menu")
    builder.row(main_menu_btn)
    #
    # ➕✍️⏱📅📆📝✉️❌⛔️⭕️❗️❕‼️🕒🔔🔕

    return builder.as_markup()
