from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from entity.models import User, Role
from handlers.menu import main_menu

router = Router()


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    user = User.get_or_none(telegram_id=message.from_user.id)
    if user is None:
        user_role = Role.get(Role.name == 'user')
        user = User.create(telegram_id=message.from_user.id,
                           name=message.from_user.username,
                           role_id=user_role.id)
    else:
        print("todo обновить псевдоним в таблице")

    await main_menu(message)
