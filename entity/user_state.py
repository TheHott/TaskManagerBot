from aiogram.fsm.state import StatesGroup, State


class CreateTaskState(StatesGroup):
    create_task_entering_text = State()
    create_task_entering_description = State()
    create_task_entering_date = State()
    create_task_entering_time = State()


class EditTaskState(StatesGroup):
    entering_new_name = State()
    entering_new_description = State()
    entering_new_date = State()
    entering_new_time = State()
