from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters import Text
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup

from tg_bot.fsm.user_fsm_handler import register_fsm
from tg_bot.keyboards import get_main_keyboard


async def user_start(message: Message, state: FSMContext):
    await message.answer("Добро пожаловать!", reply_markup=get_main_keyboard())


def register_user(dp: Dispatcher):
    register_fsm(dp=dp, cmd="Создать объявление!")
    dp.register_message_handler(user_start, commands=["start"], state="*")
    # dp.register_message_handler(cm_start, state=None)
    # dp.register_message_handler(cm_start, commands=["Создать объявление!"], state=None)
    # dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)
    # dp.register_message_handler(load_photo, content_types=['photo'], state=FSMUser.photo)
    # dp.register_message_handler(load_name, state=FSMUser.name)
    # dp.register_message_handler(load_description, state=FSMUser.description)
    # dp.register_message_handler(load_price, state=FSMUser.price)
