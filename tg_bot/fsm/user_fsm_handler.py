from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from loguru import logger

from tg_bot.fsm.classes import FSMAnnouncement
from tg_bot.keyboards import get_main_keyboard, get_fsm_start_keyboard, get_fsm_publish_keyboard, \
    get_fsm_type_task_keyboard
from tg_bot.main import get_dispatcher

dispatcher: Dispatcher = get_dispatcher()


@dispatcher.message_handler(Text('Создать объявление!'))
async def cm_start(message: Message, state: FSMContext):
    """
    Начало диалога загрузки меню
    """
    await state.reset_state()
    user = message.from_user
    logger.info(f'Start FSM, user id: {user.id}')
    await FSMAnnouncement.start.set()
    await message.answer('Привествую!\nЯ задам вам несколько вопросов и помогу правильно сформировать объявление.',
                         reply_markup=get_fsm_start_keyboard())
    print(await state.get_state())


async def load_start(message: Message, state: FSMContext):
    if message.text != 'Поехали!':
        await message.reply('Выберите ответ в меню', reply_markup=get_fsm_start_keyboard())
    else:
        async with state.proxy() as data:
            data['user_id'] = message.from_user.id

        await FSMAnnouncement.next()
        await message.reply('Из какого вы города?', reply_markup=types.ReplyKeyboardRemove())
    print(await state.get_state())


async def load_city(message: Message, state: FSMContext):
    if len(message.text) < 2:
        await message.reply('Населенный пункт введен некорректно.\nИз какого вы города?')
    else:
        async with state.proxy() as data:
            city = message.text
            data['city'] = city.replace('-', '_')

        await FSMAnnouncement.next()
        await message.answer(f'Ваш город: {city}.\n'
                             f'Какая у вас задача?', reply_markup=get_fsm_type_task_keyboard())
    print(await state.get_state())


async def publish(message: Message, state: FSMContext):
    print(message.text)
    async with state.proxy() as data:
        data['type_task'] = message.text

    async with state.proxy() as data:
        await FSMAnnouncement.next()
        await message.answer(f'Поздравляю!\nВы сформировали объявление:\n{str(data)}',
                             reply_markup=get_fsm_publish_keyboard())

    print(await state.get_state())


async def finish(message: Message, state: FSMContext):
    await cm_start(message=message, state=state)
    # await state.finish()
    # await message.answer('Ваше объявление отправлено.', reply_markup=get_main_keyboard())
    # print(type(await state.get_state()))


@dispatcher.message_handler(state='*', commands='Я передумал')
@dispatcher.message_handler(Text(equals='Я передумал', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info(f'Cancelling state: {current_state}')
    await state.finish()
    await message.reply('А вы знаете, '
                        'что в Дагестане на автомобилях нет задней передачи? '
                        'Потому что нормальные пацаны никогда не дают заднюю!',
                        reply_markup=get_main_keyboard())


async def fsm_echo(message: Message, state: FSMContext):
    print(state.proxy())


def register_fsm(dp: Dispatcher, cmd: str):
    dp.register_message_handler(cm_start, state=None)
    dp.register_message_handler(load_start, state=FSMAnnouncement.start)
    dp.register_message_handler(cancel_handler, commands=['Я передумал'], state='*')
    dp.register_message_handler(load_city, content_types=types.ContentTypes.TEXT, state=FSMAnnouncement.city)
    dp.register_message_handler(publish, state=FSMAnnouncement.publish)
    dp.register_message_handler(finish, state=FSMAnnouncement.finish)

    dp.register_message_handler(fsm_echo, state="*", content_types=types.ContentTypes.ANY)
