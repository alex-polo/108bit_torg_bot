from typing import Optional

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from tgbot.fsm.classes import FSMAnnouncement

_DISPATCHER: Dispatcher = Optional[None]
_START_CMD: str = Optional[None]


# @_DISPATCHER.message_handler(Text(_START_CMD))
@dp.message_handler(Text(_START_CMD))
async def cm_start(message: Message):
    print(11111)
    """
    Начало диалога загрузки меню
    :param message:
    :return:
    """
    await FSMAnnouncement.start.set()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text="Поехали!"))
    keyboard.add(KeyboardButton(text="Я передумал."))

    await message.answer('Привествую! Я задам вам несколько вопросов и помогу правильно сформировать объявление.',
                         reply_markup=keyboard)


def register_fsm_torgi(dp: Dispatcher, cmd: str):
    global _DISPATCHER, _START_CMD

    _DISPATCHER = dp
    _START_CMD = cmd

    dp.register_message_handler(cm_start, commands=[cmd], state=None)
