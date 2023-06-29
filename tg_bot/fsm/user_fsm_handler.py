import re

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
    back_button_text,
    get_fsm_type_equipment_consumables_keyboard,
    get_fsm_back_button_keyboard,
    get_fsm_condition_keyboard,
    get_fsm_salesman_keyboard, get_fsm_payment_type_keyboard, get_fsm_sending_to_another_city_keyboard,
    get_fsm_email_keyboard, get_fsm_photo_keyboard
)

dispatcher: Dispatcher = get_dispatcher()


# ---------------------------------------------   BACK BUTTON   -------------------------------------------------

# @dispatcher.message_handler(lambda message: message.text == back_button_text, state=FSMAnnouncement.all_states)
@exception_handler
async def event_back_button(message: Message, state: FSMContext):
    print(f'first: {await state.get_state()}')
    index_current_state = FSMAnnouncement.states_names.index(await state.get_state()) - 1
    index_current_state = index_current_state if not index_current_state < 0 else 0

    print(index_current_state)
    print(FSMAnnouncement.all_states[index_current_state])
    # await FSMAnnouncement.states[index_current_state].set()
    await state.set_state(FSMAnnouncement.all_states[index_current_state])

    print(f'second: {await state.get_state()}')

    if index_current_state == 0:
        return await cm_start(message=message, state=state)
    elif index_current_state == 1:
        return await load_start(message=message, state=state)
    elif index_current_state == 2:
        return await load_city(message=message, state=state)
    elif index_current_state == 3:
        return await load_type_task(message=message, state=state)
    elif index_current_state == 4:
        return await load_type_equipment_consumables(message=message, state=state)
    elif index_current_state == 5:
        return await load_vendor(message=message, state=state)
    elif index_current_state == 6:
        return await load_count(message=message, state=state)

    # current_state = str(await state.get_state())
    # logger.info(f'Press back button, user id: {message.from_user.id}, current state: {current_state}')
    # if current_state == 'FSMAnnouncement:city':
    #     await state.set_state(FSMAnnouncement.start)
    #     await FSMAnnouncement.first()
    #     return await cm_start(message=message, state=state)
    #
    # elif current_state == 'FSMAnnouncement:type_task':
    #     await state.set_state(FSMAnnouncement.city)
    #     await FSMAnnouncement.start.set()
    #     return await load_start(message=message, state=state)
    #
    # elif current_state == 'FSMAnnouncement:type_equipment_consumables':
    #     await state.set_state(FSMAnnouncement.type_task)
    #     await FSMAnnouncement.city.set()
    #     return await load_city(message=message, state=state)
    #
    # elif current_state == 'FSMAnnouncement:vendor':
    #     await state.set_state(FSMAnnouncement.type_task)
    #     await FSMAnnouncement.type_task.set()
    #     return await load_type_task(message=message, state=state)
    #
    # elif current_state == 'FSMAnnouncement:count':
    #     await state.set_state(FSMAnnouncement.type_equipment_consumables)
    #     await FSMAnnouncement.type_equipment_consumables.set()
    #     return await load_type_equipment_consumables(message=message, state=state)
    #
    # elif current_state == 'FSMAnnouncement:condition':
    #     await state.set_state(FSMAnnouncement.vendor)
    #     await FSMAnnouncement.vendor.set()
    #     return await load_vendor(message=message, state=state)

    """
    start = State()
    city = State()
    type_task = State()
    type_equipment_consumables = State()
    vendor = State()
    count = State()
    condition = State()
    """


# count
@exception_handler
async def choose_an_answer_from_the_menu(message: Message, state: FSMContext):
    return await message.reply('Выберите ответ в меню')


@exception_handler
async def cm_start(message: Message, state: FSMContext):
    logger.info(f'Start FSM, state: {await state.get_state()}, user id: {message.from_user.id}')
    # await state.reset_state()
    await FSMAnnouncement.start.set()
    await message.answer('Привествую!\nЯ задам вам несколько вопросов и помогу правильно сформировать объявление.',
                         reply_markup=get_fsm_start_keyboard())


# ---------------------------------------------   START   -------------------------------------------------
@exception_handler
async def load_start(message: Message, state: FSMContext):
    logger.info(f'Load start FSM, state: {await state.get_state()}, user id: {message.from_user.id}')
    await FSMAnnouncement.next()
    await message.answer('Из какого вы города?', reply_markup=get_fsm_back_button_keyboard())


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
    return await message.reply('Населенный пункт введен некорректно.\n\nИз какого вы города?',
                               reply_markup=get_fsm_back_button_keyboard())


@exception_handler
async def load_city(message: Message, state: FSMContext):
    logger.info(f'Load city, state: {await state.get_state()}, city: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            city = message.text.title()
            data['city'] = city
        else:
            city = data['city']

    await FSMAnnouncement.next()
    await message.answer(f'Ваш город: {city}.\n\n'
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
        if message.text != back_button_text:
            type_task = message.text.split(' ')[-1].title()
            data['type_task'] = type_task
        else:
            type_task = data['type_task']

    await FSMAnnouncement.next()
    await message.answer(f'Вы хотите: {type_task}.\n\n'
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
        if message.text != back_button_text:
            type_equipment_consumables = message.text
            data['type_equipment_consumables'] = type_equipment_consumables
        else:
            type_equipment_consumables = data['type_equipment_consumables']

    await FSMAnnouncement.next()
    await message.answer(f'Тип оборудования/расходных материалов:\n{type_equipment_consumables}.\n\n'
                         f'Укажите производителя:',
                         reply_markup=get_fsm_back_button_keyboard())


# --------------------------------------------   LOAD VENDOR   ---------------------------------------------------
@exception_handler
async def load_vendor_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load vendor, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Некорректно указан производитель.\nУкажите производителя:',
                               reply_markup=get_fsm_back_button_keyboard())


@exception_handler
async def load_vendor(message: Message, state: FSMContext):
    logger.info(f'Load vendor, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            vendor = message.text
            data['vendor'] = vendor
        else:
            vendor = data['vendor']

    await FSMAnnouncement.next()
    await message.answer(f'Производитель: {vendor}.\n\n'
                         f'Укажите количество единиц (число):',
                         reply_markup=get_fsm_back_button_keyboard())


# --------------------------------------------   LOAD COUNT   ---------------------------------------------------
@exception_handler
async def load_count_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load count, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Некорректно указано количество.\n\nУкажите количество единиц (число):',
                               reply_markup=get_fsm_back_button_keyboard())


@exception_handler
async def load_count(message: Message, state: FSMContext):
    logger.info(f'Load count, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            count = message.text
            data['count'] = count
        else:
            count = data['count']

    await FSMAnnouncement.next()
    await message.answer(f'Указанное количество: {count}.\n\n'
                         f'Укажите состояние:',
                         reply_markup=get_fsm_condition_keyboard())


# ---------------------------------------------   LOAD CONDITION   -------------------------------------------------
@exception_handler
async def load_condition_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load condition, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Неверно указано состояние.\nВыберите один из пунктов меню:',
                               reply_markup=get_fsm_condition_keyboard())


@exception_handler
async def load_condition(message: Message, state: FSMContext):
    logger.info(f'Load condition, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            condition = message.text
            data['condition'] = condition
        else:
            condition = data['condition']

    await FSMAnnouncement.next()
    await message.answer(f'Состояние: {condition}.\n\nВы представитель компании или частное лицо?:',
                         reply_markup=get_fsm_salesman_keyboard())


# ---------------------------------------------   LOAD SALESMAN   -------------------------------------------------

@exception_handler
async def load_salesman_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid salesman count, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Неверно указан представитель.\nВыберите один из пунктов меню:',
                               reply_markup=get_fsm_salesman_keyboard())


@exception_handler
async def load_salesman(message: Message, state: FSMContext):
    logger.info(f'Load salesman, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            salesman = message.text
            data['salesman'] = salesman
        else:
            salesman = data['salesman']

    await FSMAnnouncement.next()
    await message.answer(f'Выбранный представитель: {salesman}.\n\nУкажите стоимость (число в рублях):',
                         reply_markup=get_fsm_back_button_keyboard())


# ---------------------------------------------   LOAD PRICE   -------------------------------------------------
@exception_handler
async def load_price_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid price count, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Неверно указана стоимость.\nУкажите число в рублях:',
                               reply_markup=get_fsm_back_button_keyboard())


@exception_handler
async def load_price(message: Message, state: FSMContext):
    logger.info(f'Load price, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            price = message.text
            data['price'] = price
        else:
            price = data['price']

    await FSMAnnouncement.next()
    await message.answer(f'Указана стоимость: {price} руб.\n\nУкажите тип оплаты:',
                         reply_markup=get_fsm_payment_type_keyboard())


# ---------------------------------------------   LOAD PAYMENT TYPE   -------------------------------------------------
@exception_handler
async def load_payment_type_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid payment type, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Укажите возможность доставки:',
                               reply_markup=get_fsm_payment_type_keyboard())


@exception_handler
async def load_payment_type(message: Message, state: FSMContext):
    logger.info(f'Load payment type, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            payment_type = message.text
            data['payment_type'] = payment_type
        else:
            payment_type = data['payment_type']

    await FSMAnnouncement.next()
    if data['type_task'] == 'Купить':
        async with state.proxy() as data:
            data['sending_to_another_city'] = 'no_use'

        await FSMAnnouncement.next()
        await message.answer(f'Укажите электронную почту для связи:',
                             reply_markup=get_fsm_back_button_keyboard())
    else:
        await message.answer(f'Выбран тип оплаты: {payment_type}.\n\nЕсть ли отправка в другой город?:',
                             reply_markup=get_fsm_sending_to_another_city_keyboard())


# ----------------------------------   LOAD SENDING TO ANOTHER CITY   ---------------------------------------
@exception_handler
async def load_sending_to_another_city_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid sending_to_another_city, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Укажите возможность доставки:',
                               reply_markup=get_fsm_sending_to_another_city_keyboard())


@exception_handler
async def load_sending_to_another_city(message: Message, state: FSMContext):
    logger.info(f'Load sending_to_another_city, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if data['type_task'] == 'Купить':
            await FSMAnnouncement.next()
        else:
            if message.text != back_button_text:
                sending_to_another_city = message.text
                data['sending_to_another_city'] = sending_to_another_city
            else:
                sending_to_another_city = data['sending_to_another_city']

            await FSMAnnouncement.next()
            await message.answer(f'Возможность доставки в другой город: {sending_to_another_city}.'
                                 f'\n\nУкажите электронную почту для связи:',
                                 reply_markup=get_fsm_email_keyboard())


# ---------------------------------------------   LOAD EMAIL   ---------------------------------------------
@exception_handler
async def load_email_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load email, text: {message.text}, user id: {message.from_user.id}')
    return await message.reply('Укажите электронную почту для связи:',
                               reply_markup=get_fsm_email_keyboard())


@exception_handler
async def load_email(message: Message, state: FSMContext):
    logger.info(f'Load email, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            if message.text == 'Пропустить':
                data['email'] = 'no_use'
            else:
                email = message.text
                data['email'] = email
        else:
            email = data['email']

        await FSMAnnouncement.next()
        await message.answer(f'Указан E-mail: {email}.'
                             f'\n\nУкажите контактный телефон для связи:',
                             reply_markup=get_fsm_back_button_keyboard())


# ---------------------------------------------   LOAD PHONE   ---------------------------------------------
@exception_handler
async def load_phone_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load phone, text: {message.text}, user id: {message.from_user.id}')
    return await message.answer(f'Некорректно указан телефонный номер.\n\nУкажите контактный телефон для связи:',
                                reply_markup=get_fsm_back_button_keyboard())


@exception_handler
async def load_phone(message: Message, state: FSMContext):
    logger.info(f'Load phone, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            phone = message.text
            data['phone'] = phone
        else:
            phone = data['phone']

        await FSMAnnouncement.next()
        await message.answer(f'Указанный телефон: {phone}.\n\n'
                             f'Кратко опишите модель оборудования, условия оплаты, '
                             f'доставки и другую необходимую информацию (допускается до 200 символов):',
                             reply_markup=get_fsm_back_button_keyboard())


# ---------------------------------------------   LOAD DETAILS   ---------------------------------------------
@exception_handler
async def load_details_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load details, text: {message.text}, user id: {message.from_user.id}')
    return await message.answer(f'Некорректно указана дополнительная информация ((допускается до 200 символов)),'
                                f'попробуйте еще раз:',
                                reply_markup=get_fsm_back_button_keyboard())


@exception_handler
async def load_details(message: Message, state: FSMContext):
    logger.info(f'Load details, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            details = message.text
            data['details'] = details
        else:
            details = data['details']

        await FSMAnnouncement.next()
        await message.answer(f'Дополнительная информация:\n {details}.\n\n'
                             f'Приложите фото:',
                             reply_markup=get_fsm_photo_keyboard())



# ---------------------------------------------   LOAD PHOTO   ---------------------------------------------
@exception_handler
async def load_photo_ignore(message: types.Message, state: FSMContext):
    logger.info(f'Invalid load photo, text: {message.text}, user id: {message.from_user.id}')
    return await message.answer(f'Некорректно указано изображение, попробуйте еще раз:',
                                reply_markup=get_fsm_photo_keyboard())


@exception_handler
async def load_photo(message: Message, state: FSMContext):
    logger.info(f'Load details, text: {message.text}. user id: {message.from_user.id}')
    async with state.proxy() as data:
        if message.text != back_button_text:
            photo = message.text
            data['photo'] = photo
        else:
            photo = data['photo']

        await FSMAnnouncement.next()
        await message.answer(f'Изображение:\n {photo}.\n\n',
                             reply_markup=get_fsm_photo_keyboard())


# ---------------------------------------------   LOAD PUBLISH   -------------------------------------------------
@exception_handler
async def publish(message: Message, state: FSMContext):
    # async with state.proxy() as data:
    #     data['type_task'] = message.text

    # raise Exception('sssssssssssssssss')

    async with state.proxy() as data:
        await FSMAnnouncement.next()
        await message.answer(f'Поздравляю!\nВы сформировали объявление:\n{str(data)}',
                             reply_markup=get_fsm_publish_keyboard())


# ---------------------------------------------   FSM FINISH   -------------------------------------------------
@exception_handler
async def finish(message: Message, state: FSMContext):
    # await cm_start(message=message, state=state)
    await state.finish()
    await message.answer('Ваше объявление отправлено.', reply_markup=get_main_keyboard())


# ---------------------------------------------   REGISTRY FSM   -------------------------------------------------
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
                                                message.text == 'Сервера, ПК, комплектующие' or
                                                message.text == back_button_text,
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

    dp.register_message_handler(load_condition,
                                lambda message: message.text == 'Новое' or message.text == 'Б/У',
                                state=FSMAnnouncement.condition)
    dp.register_message_handler(load_condition_ignore, state=FSMAnnouncement.condition)

    dp.register_message_handler(load_salesman,
                                lambda message: message.text == 'Компания' or message.text == 'Частное лицо',
                                state=FSMAnnouncement.salesman)
    dp.register_message_handler(load_salesman_ignore, state=FSMAnnouncement.salesman)

    dp.register_message_handler(load_price, lambda message: message.text.isdigit(), state=FSMAnnouncement.price)
    dp.register_message_handler(load_price_ignore, state=FSMAnnouncement.price)

    dp.register_message_handler(load_payment_type,
                                lambda message: message.text == 'Наличные' or
                                                message.text == 'Безналичные' or
                                                message.text == 'Нал/Безнал',
                                state=FSMAnnouncement.payment_type)
    dp.register_message_handler(load_payment_type_ignore, state=FSMAnnouncement.payment_type)

    dp.register_message_handler(load_sending_to_another_city,
                                lambda message: message.text == 'Да' or
                                                message.text == 'Нет',
                                state=FSMAnnouncement.sending_to_another_city)
    dp.register_message_handler(load_sending_to_another_city_ignore, state=FSMAnnouncement.sending_to_another_city)

    dp.register_message_handler(load_email,
                                lambda message: re.match(r"^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$", message.text),
                                state=FSMAnnouncement.email)
    dp.register_message_handler(load_email_ignore, state=FSMAnnouncement.email)

    dp.register_message_handler(load_phone, lambda message: len(message.text) > 2, state=FSMAnnouncement.phone)
    dp.register_message_handler(load_phone_ignore, state=FSMAnnouncement.phone)

    dp.register_message_handler(load_details, lambda message: 0 < len(message.text) <= 200,
                                state=FSMAnnouncement.details)
    dp.register_message_handler(load_details_ignore, state=FSMAnnouncement.details)

    dp.register_message_handler(load_photo,
                                # lambda message: 0 < len(message.text) <= 200,
                                state=FSMAnnouncement.details)
    dp.register_message_handler(load_photo_ignore, state=FSMAnnouncement.details)

    # @dispatcher.message_handler(lambda message: message.text == back_button_text, state=FSMAnnouncement.all_states)
    # dp.register_message_handler(load_start, state=FSMAnnouncement.start)

    dp.register_message_handler(publish, state=FSMAnnouncement.publish)
    dp.register_message_handler(finish, state=FSMAnnouncement.finish)
