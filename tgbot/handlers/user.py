import types

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup

from tgbot.fsm import register_fsm_torgi
from tgbot.fsm.classes import FSMAnnouncement


class FSMUser(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


# Начало диалога загрузки меню
async def cm_start(message: Message):
    await FSMUser.photo.set()
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text="Поехали!"))
    # keyboard.
    # await bot.send_message(message.chat.id, text=query, parse_mode='HTML',
    #                        reply_markup=reply)
    await message.reply('Загрузи фото', reply_markup=keyboard)


# Ловим первый ответ от пользователя
async def load_photo(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        print(data)
    await FSMUser.next()
    await message.reply('Теперь введи название')


async def load_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMUser.next()
    await message.reply('Введите описание')


async def load_description(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await FSMUser.next()
    await message.reply('Теперь укажите цену')


async def load_price(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    async with state.proxy() as data:
        await message.reply(str(data))
    await state.finish()
    # await message.reply('Поздравляю! Вы сформировали объявление. ')


async def user_start(message: Message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text="Создать объявление!"))
    await message.answer("Добро пожаловать!", reply_markup=keyboard)


def register_user(dp: Dispatcher):
    register_fsm_torgi(dp=dp, cmd="Создать объявление!")
    dp.register_message_handler(user_start, commands=["start"], state="*")
    # dp.register_message_handler(cm_start, commands=["Создать объявление!"], state=None)
    # dp.register_message_handler(cm_start, commands=["Загрузить"], state=None)
    # dp.register_message_handler(load_photo, content_types=['photo'], state=FSMUser.photo)
    # dp.register_message_handler(load_name, state=FSMUser.name)
    # dp.register_message_handler(load_description, state=FSMUser.description)
    # dp.register_message_handler(load_price, state=FSMUser.price)
