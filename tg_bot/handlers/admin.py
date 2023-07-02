from typing import Optional

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger

from tg_bot.fsm.user_fsm_handler import register_fsm
from tg_bot.keyboards import get_main_keyboard

_shutdown_callback = Optional[None]


async def admin_start(message: Message, state: FSMContext):
    logger.info(f'Admin user is id: {message.from_user.id} press start command')
    await state.reset_state()
    await message.answer("Добро пожаловать!", reply_markup=get_main_keyboard())


async def admin_shutdown(message: Message, state: FSMContext):
    logger.info(f'Admin user is id: {message.from_user.id} press shutdown button')
    await message.reply('Пока')
    await _shutdown_callback()


def register_admin(dp: Dispatcher, shutdown_callback):
    logger.info('Register admins handlers')

    global _shutdown_callback
    _shutdown_callback = shutdown_callback

    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(admin_shutdown, commands=["bot_stop"], state="*", is_admin=True)
    register_fsm(dp=dp)
