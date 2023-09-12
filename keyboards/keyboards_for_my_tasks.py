import math

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


PAGE_SIZE = 5


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
                                         callback_data="show_task#" + str(task.get_id())))

    if page == 1:
        first_page_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
        previous_page_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
    else:
        first_page_btn = InlineKeyboardButton(text="⏮", callback_data=prefix + "_page#1")
        previous_page_btn = InlineKeyboardButton(text="◀️", callback_data=prefix + "_page#" + str(page - 1))
    page_count_btn = InlineKeyboardButton(text=str(page) + '/' + str(amount_of_pages),
                                          callback_data="enter_page_number")
    if page == amount_of_pages:
        next_page_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
        last_page_btn = InlineKeyboardButton(text=" ", callback_data="no_action")
    else:
        next_page_btn = InlineKeyboardButton(text="▶️", callback_data=prefix + "_page#" + str(page + 1))
        last_page_btn = InlineKeyboardButton(text="⏭", callback_data=prefix + "_page#" + str(amount_of_pages))
    builder.row(first_page_btn, previous_page_btn, page_count_btn, next_page_btn, last_page_btn)

    main_menu_btn = InlineKeyboardButton(text="На главную", callback_data="main_menu")
    builder.row(main_menu_btn)
    #
    # ➕✍️⏱📅📆📝✉️❌⛔️⭕️❗️❕‼️🕒🔔🔕

    return builder.as_markup()
