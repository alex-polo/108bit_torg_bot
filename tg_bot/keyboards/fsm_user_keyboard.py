from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_button_text = '⬅️ Назад'


def get_fsm_back_button_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.row(KeyboardButton(text=back_button_text))
    return keyboard


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton(text="Опубликовать объявление"))
    return keyboard


def get_fsm_start_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    keyboard.add(KeyboardButton(text="Поехали"))
    keyboard.add(KeyboardButton(text="Я передумал"))
    return keyboard


def get_fsm_condition_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text='Новое'))
    keyboard.add(KeyboardButton(text='Б/У'))
    keyboard.add(KeyboardButton(text=back_button_text))
    return keyboard


def get_fsm_type_task_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text='Хочу продать'))
    keyboard.add(KeyboardButton(text='Хочу купить'))
    keyboard.add(KeyboardButton(text=back_button_text))
    return keyboard


def get_fsm_type_equipment_consumables_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    keyboard.insert(KeyboardButton(text='Системы безопасности'))
    keyboard.insert(KeyboardButton(text='Автоматика и КИПиА'))
    keyboard.insert(KeyboardButton(text='Электрика'))
    keyboard.insert(KeyboardButton(text='Телеком и связь'))
    keyboard.insert(KeyboardButton(text='Сервера, ПК, комплектующие'))
    keyboard.row(KeyboardButton(text=back_button_text))
    return keyboard


def get_fsm_publish_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text="Опубликовать"))
    keyboard.add(KeyboardButton(text=back_button_text))
    return keyboard


def get_fsm_salesman_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.insert(KeyboardButton(text='Компания'))
    keyboard.insert(KeyboardButton(text='Частное лицо'))
    keyboard.row(KeyboardButton(text=back_button_text))
    return keyboard


def get_fsm_payment_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.insert(KeyboardButton(text='Наличные')),
    keyboard.insert(KeyboardButton(text='Безналичные'))
    keyboard.insert(KeyboardButton(text='Нал/Безнал'))
    keyboard.row(KeyboardButton(text=back_button_text))
    return keyboard


def get_fsm_sending_to_another_city_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.insert(KeyboardButton(text='Да')),
    keyboard.insert(KeyboardButton(text='Нет'))
    keyboard.row(KeyboardButton(text=back_button_text))
    return keyboard
