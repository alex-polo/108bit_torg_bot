import traceback

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from loguru import logger

from tg_bot.fsm.classes import FSMAnnouncement
from tg_bot.keyboards import get_main_keyboard, get_fsm_start_keyboard, get_fsm_publish_keyboard, \
    get_fsm_type_task_keyboard
from tg_bot.main import get_dispatcher

dispatcher: Dispatcher = get_dispatcher()


async def choose_an_answer_from_the_menu(message: Message):
    return await message.reply('Выберите ответ в меню', reply_markup=get_fsm_start_keyboard())


@dispatcher.message_handler(Text('Создать объявление!'))
async def cm_start(message: Message, state: FSMContext):
    """
    Начало диалога загрузки меню
    """
    try:
        await state.reset_state()
        logger.info(f'Start FSM, user id: {message.from_user.id}')
        await FSMAnnouncement.start.set()
        await message.answer('Привествую!\nЯ задам вам несколько вопросов и помогу правильно сформировать объявление.',
                             reply_markup=get_fsm_start_keyboard())
    except Exception as error:
        logger.error(error)
        logger.error(traceback.format_exc(limit=None, chain=True))
        await exception_handler(message=message, state=state)


#########################################   START   ####################################################
@dispatcher.message_handler(lambda message: not message.text == 'Поехали!', state=FSMAnnouncement.start)
async def cm_start_invalid(message: types.Message):
    logger.info(f'Invalid load start FSM, user id: {message.from_user.id}')
    return choose_an_answer_from_the_menu(message=message)


async def load_start(message: Message, state: FSMContext):
    logger.info(f'Load start FSM, user id: {message.from_user.id}')
    await FSMAnnouncement.next()
    await message.reply('Из какого вы города?', reply_markup=types.ReplyKeyboardRemove())


#########################################   LOAD CITY   ####################################################
@dispatcher.message_handler(lambda message: not len(message.text) > 2, state=FSMAnnouncement.city)
async def load_city_ignore(message: types.Message):
    logger.info(f'Invalid load city, city: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Населенный пункт введен некорректно.\nИз какого вы города?')


async def load_city(message: Message, state: FSMContext):
    logger.info(f'Load city, city: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        city = message.text
        data['city'] = city.replace('-', '_')

    await FSMAnnouncement.next()
    await message.answer(f'Ваш город: {city}.\n'
                         f'Какая у вас задача?', reply_markup=get_fsm_type_task_keyboard())


#########################################   LOAD PUBLISH   ####################################################
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


#########################################   CANCELEDED   ####################################################
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


#########################################   EXCEPTION   ####################################################
async def exception_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    logger.error(f'Exception state: {current_state}')
    await state.reset_state()
    await message.reply('Ууууупппс, произошла ошибка, попробуйте еще раз', reply_markup=get_main_keyboard())


# async def fsm_echo(message: Message, state: FSMContext):
#     print(state.proxy())


def register_fsm(dp: Dispatcher, cmd: str):
    dp.register_message_handler(cm_start, state=None)
    dp.register_message_handler(load_start, state=FSMAnnouncement.start)
    dp.register_message_handler(cancel_handler, commands=['Я передумал'], state='*')
    dp.register_message_handler(load_city, content_types=types.ContentTypes.TEXT, state=FSMAnnouncement.city)
    dp.register_message_handler(publish, state=FSMAnnouncement.publish)
    dp.register_message_handler(finish, state=FSMAnnouncement.finish)

    dp.register_message_handler(fsm_echo, state="*", content_types=types.ContentTypes.ANY)
