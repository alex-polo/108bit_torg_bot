from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hcode
from loguru import logger


async def bot_echo(message: types.Message):
    # text = [
    #     "Эхо без состояния.",
    #     "Сообщение:",
    #     message.text
    # ]
    #
    # await message.answer('\n'.join(text))
    logger.debug(f'Echo without state, user id: {message.from_user.id}')


async def bot_echo_all(message: types.Message, state: FSMContext):
    # state_name = await state.get_state()
    # text = [
    #     f'Эхо в состоянии {hcode(state_name)}',
    #     'Содержание сообщения:',
    #     hcode(message.text)
    # ]
    # await message.answer('\n'.join(text))
    logger.debug(f'Echo with state, user id: {message.from_user.id}, state: {await state.get_state()}')


def register_echo(dp: Dispatcher):
    dp.register_message_handler(bot_echo)
    dp.register_message_handler(bot_echo_all, state="*", content_types=types.ContentTypes.ANY)
