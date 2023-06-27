import traceback

from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger

from tg_bot.keyboards import get_main_keyboard


async def exception_event(message: Message, state: FSMContext = None):
    if state is not None:
        await state.reset_state()
    await message.reply('Ууууупппс, произошла непредвиденная ошибка, попробуйте еще раз',
                        reply_markup=get_main_keyboard())


def exception_handler(function):
    async def wrapper(message: Message, state: FSMContext = None):
        try:
            await function(message, state)
        except Exception as error:
            logger.error(error)
            logger.error(traceback.format_exc(limit=None, chain=True))
            await exception_event(message=message, state=state)

    return wrapper
