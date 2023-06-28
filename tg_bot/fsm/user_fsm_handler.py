from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from loguru import logger

from tg_bot.fsm.classes import FSMAnnouncement
from tg_bot.fsm.exceptions import exception_handler
from tg_bot.main import get_dispatcher

from tg_bot.keyboards import (
    get_main_keyboard,
    get_fsm_start_keyboard,
    get_fsm_publish_keyboard,
    get_fsm_type_task_keyboard,
    get_fsm_city_keyboard,
    back_button_text,
    get_fsm_type_equipment_consumables_keyboard,
    get_fsm_vendor_keyboard
)

dispatcher: Dispatcher = get_dispatcher()


# ---------------------------------------------   BACK BUTTON   -------------------------------------------------
@exception_handler
# @dispatcher.message_handler(lambda message: message.text == back_button_text, state=FSMAnnouncement.all_states)
async def event_back_button(message: Message, state: FSMContext):
    current_state = str(await state.get_state())
    logger.info(f'Press back button, user id: {message.from_user.id}, current state: {current_state}')
    if current_state == 'FSMAnnouncement:city':
        await state.set_state(FSMAnnouncement.start)
        await FSMAnnouncement.first()
        return await cm_start(message=message, state=state)

    elif current_state == 'FSMAnnouncement:type_task':
        await state.set_state(FSMAnnouncement.city)
        await FSMAnnouncement.start.set()
        return await load_start(message=message, state=state)

    elif current_state == 'FSMAnnouncement:type_equipment_consumables':
        await state.set_state(FSMAnnouncement.type_task)
        await FSMAnnouncement.city.set()
        return await load_city(message=message, state=state)

    elif current_state == 'FSMAnnouncement:vendor':
        await state.set_state(FSMAnnouncement.type_task)
        await FSMAnnouncement.type_task.set()
        return await load_type_task(message=message, state=state)

    elif current_state == 'FSMAnnouncement:count':
        await state.set_state(FSMAnnouncement.type_equipment_consumables)
        await FSMAnnouncement.type_equipment_consumables.set()
        return await load_type_equipment_consumables_ignore(message=message, state=state)

    elif current_state == 'FSMAnnouncement:condition':
        await state.set_state(FSMAnnouncement.vendor)
        await FSMAnnouncement.vendor.set()
        return await load_vendor(message=message, state=state)


# count
@exception_handler
async def choose_an_answer_from_the_menu(message: Message, state: FSMContext):
    return await message.reply('Выберите ответ в меню')


@exception_handler
async def cm_start(message: Message, state: FSMContext):
    logger.info(f'Start FSM, state: {await state.get_state()}, user id: {message.from_user.id}')
    await state.reset_state()
    await FSMAnnouncement.start.set()
    await message.answer('Привествую!\nЯ задам вам несколько вопросов и помогу правильно сформировать объявление.',
                         reply_markup=get_fsm_start_keyboard())


# ---------------------------------------------   START   -------------------------------------------------
@exception_handler
async def load_start(message: Message, state: FSMContext):
    logger.info(f'Load start FSM, state: {await state.get_state()}, user id: {message.from_user.id}')
    await FSMAnnouncement.next()
    await message.answer('Из какого вы города?', reply_markup=get_fsm_city_keyboard())


@exception_handler
@dispatcher.message_handler(commands='Я передумал', state=FSMAnnouncement.start, )
@dispatcher.message_handler(Text(equals='Я передумал', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logger.info(f'Cancelling state: {current_state}')
    await state.finish()
    await message.reply('А вы знаете, '
                        'что в Дагестане на автомобилях нет задней передачи? '
                        'Потому, что нормальные пацаны никогда не дают заднюю!',
                        reply_markup=get_main_keyboard())


@exception_handler
# @dispatcher.message_handler(lambda message: not message.text == 'Поехали', state=FSMAnnouncement.start)
async def cm_start_invalid(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load start FSM, state: {await state.get_state()}, user id: {message.from_user.id}')
    return await choose_an_answer_from_the_menu(message=message)


# ---------------------------------------------   LOAD CITY   -------------------------------------------------
@exception_handler
async def load_city_ignore(message: types.Message, state: FSMContext):
    logger.info(
        f'Invalid load city, state: {await state.get_state()}, city: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Населенный пункт введен некорректно.\nИз какого вы города?',
                               reply_markup=get_fsm_city_keyboard())


@exception_handler
async def load_city(message: Message, state: FSMContext):
    logger.info(f'Load city, state: {await state.get_state()}, city: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        data['city'] = message.text

    await FSMAnnouncement.next()
    await message.answer(f'Ваш город: {message.text}.\n'
                         f'Какая у вас задача?', reply_markup=get_fsm_type_task_keyboard())


# ---------------------------------------------   LOAD TYPE TASK   -------------------------------------------------
@exception_handler
async def load_type_task_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid type task, type task: {message.text}, user id: {message.from_user.id}')
    return await choose_an_answer_from_the_menu(message=message)


@exception_handler
async def load_type_task(message: Message, state: FSMContext):
    logger.info(f'Load type task, type task: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        data['type_task'] = message.text

    await FSMAnnouncement.next()
    await message.answer(f'Вы хотите: {message.text}.\n\n'
                         f'Какой тип оборудования/расходных материалов вы предлагаете/ищете?',
                         reply_markup=get_fsm_type_equipment_consumables_keyboard())


# ----------------------------------   LOAD TYPE EQUIPMENT CONSUMABLES   ----------------------------------------
@exception_handler
async def load_type_equipment_consumables_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid type equipment consumables, text: {message.text}, user id: {message.from_user.id}')
    return await choose_an_answer_from_the_menu(message=message)


@exception_handler
async def load_type_equipment_consumables(message: Message, state: FSMContext):
    logger.info(f'Load type equipment consumables, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        data['type_equipment_consumables'] = message.text

    await FSMAnnouncement.next()
    await message.answer(f'Тип оборудования/расходных материалов: {message.text}.\n\n'
                         f'Укажите производителя:',
                         reply_markup=get_fsm_vendor_keyboard())


# --------------------------------------------   LOAD VENDOR   ---------------------------------------------------
@exception_handler
async def load_vendor_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load vendor, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Некорректно указан производитель.\nУкажите производителя:',
                               reply_markup=get_fsm_vendor_keyboard())


@exception_handler
async def load_vendor(message: Message, state: FSMContext):
    logger.info(f'Load vendor, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        data['type_equipment_consumables'] = message.text

    await FSMAnnouncement.next()
    await message.answer(f'Производитель: {message.text}.\n\n'
                         f'Укажите количество единиц (число):',
                         reply_markup=get_fsm_vendor_keyboard())


# --------------------------------------------   LOAD COUNT   ---------------------------------------------------
@exception_handler
async def load_count_ignore(message: types.Message):
    logger.info(f'Invalid load count, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Некорректно указано количество.\nУкажите количество единиц (число):',
                               reply_markup=get_fsm_vendor_keyboard())


@exception_handler
async def load_count(message: Message, state: FSMContext):
    logger.info(f'Load vendor, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        data['type_equipment_consumables'] = message.text

    await FSMAnnouncement.next()
    await message.answer(f'Указанное количество: {message.text}.\n\n'
                         f'Укажите состояние::',
                         reply_markup=get_fsm_vendor_keyboard())


#########################################   LOAD condition   ####################################################
@exception_handler
async def load_count_ignore(message: types.Message):
    logger.info(f'Invalid load count, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Некорректно указано количество.\nУкажите количество единиц (число):',
                               reply_markup=get_fsm_vendor_keyboard())


@exception_handler
async def load_count(message: Message, state: FSMContext):
    logger.info(f'Load vendor, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        data['type_equipment_consumables'] = message.text

    await FSMAnnouncement.next()
    await message.answer(f'Производитель: {message.text}.\n\n'
                         f'Укажите количество единиц (число):',
                         reply_markup=get_fsm_vendor_keyboard())


#########################################   LOAD PUBLISH   ####################################################
@exception_handler
async def publish(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['type_task'] = message.text

    raise Exception('sssssssssssssssss')

    async with state.proxy() as data:
        await FSMAnnouncement.next()
        await message.answer(f'Поздравляю!\nВы сформировали объявление:\n{str(data)}',
                             reply_markup=get_fsm_publish_keyboard())


@exception_handler
async def finish(message: Message, state: FSMContext):
    # await cm_start(message=message, state=state)
    await state.finish()
    await message.answer('Ваше объявление отправлено.', reply_markup=get_main_keyboard())


def register_fsm(dp: Dispatcher):
    logger.info('Registration FSMAnnouncement handlers for user')

    dp.register_message_handler(cm_start, commands=['post_ad'], state=None)
    dp.register_message_handler(cm_start, Text(equals='Опубликовать объявление'), state=None)
    dp.register_message_handler(event_back_button, Text(equals=back_button_text), state=FSMAnnouncement.all_states)

    dp.register_message_handler(load_start, Text(equals='Поехали'), state=FSMAnnouncement.start)
    dp.register_message_handler(cm_start_invalid, state=FSMAnnouncement.start)

    dp.register_message_handler(load_city,
                                lambda message: len(message.text) > 2,
                                content_types=types.ContentTypes.TEXT, state=FSMAnnouncement.city)
    dp.register_message_handler(load_city_ignore, state=FSMAnnouncement.city)

    dp.register_message_handler(load_type_task,
                                lambda message: message.text == 'Хочу купить' or message.text == 'Хочу продать',
                                content_types=types.ContentTypes.TEXT, state=FSMAnnouncement.type_task)
    dp.register_message_handler(load_type_task_ignore, state=FSMAnnouncement.type_task)

    dp.register_message_handler(load_type_equipment_consumables,
                                lambda message: message.text == 'Системы безопасности' or
                                                message.text == 'Автоматика и КИПиА' or
                                                message.text == 'Электрика' or
                                                message.text == 'Телеком и связь' or
                                                message.text == 'Сервера, ПК, комплектующие',
                                content_types=types.ContentTypes.TEXT,
                                state=FSMAnnouncement.type_equipment_consumables)
    dp.register_message_handler(load_type_equipment_consumables_ignore,
                                state=FSMAnnouncement.type_equipment_consumables)

    dp.register_message_handler(load_vendor,
                                lambda message: len(message.text) > 2,
                                content_types=types.ContentTypes.TEXT, state=FSMAnnouncement.vendor)
    dp.register_message_handler(load_vendor_ignore, state=FSMAnnouncement.vendor)

    dp.register_message_handler(load_count, lambda message: message.text.isdigit(), state=FSMAnnouncement.count)
    dp.register_message_handler(load_count_ignore, state=FSMAnnouncement.count)

    # @dispatcher.message_handler(lambda message: message.text == back_button_text, state=FSMAnnouncement.all_states)
    # dp.register_message_handler(load_start, state=FSMAnnouncement.start)

    dp.register_message_handler(publish, state=FSMAnnouncement.publish)
    dp.register_message_handler(finish, state=FSMAnnouncement.finish)
