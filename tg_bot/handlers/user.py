import asyncio
from typing import Optional

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger

from tg_bot.fsm.user_fsm_handler import register_fsm
from tg_bot.keyboards import get_main_keyboard

_DISPATCHER: Dispatcher = Optional[None]


async def user_start(message: Message, state: FSMContext):
    logger.info(f'User is id: {message.from_user.id} press start command')
    await state.reset_state()
    await message.answer("Добро пожаловать!", reply_markup=get_main_keyboard())


def register_user(dp: Dispatcher):
    global _DISPATCHER
    _DISPATCHER = dp

    dp.register_message_handler(user_start, commands=['start'], state='*')
    register_fsm(dp=dp)
