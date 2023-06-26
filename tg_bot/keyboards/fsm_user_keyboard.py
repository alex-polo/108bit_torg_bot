from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_button_text = '⬅️ Назад'


def get_main_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text="Создать объявление!"))
    return keyboard


def get_fsm_start_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text="Поехали!"))
    keyboard.add(KeyboardButton(text="Я передумал"))
    return keyboard


def get_fsm_city_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text=back_button_text))
    return keyboard


def get_fsm_type_task_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text="Хочу продать"))
    keyboard.add(KeyboardButton(text='Хочу купить'))
    keyboard.add(KeyboardButton(text=back_button_text))
    return keyboard


def get_fsm_publish_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(KeyboardButton(text="Опубликовать"))
    keyboard.add(KeyboardButton(text=back_button_text))
    return keyboard
