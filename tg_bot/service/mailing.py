import asyncio
import datetime
import traceback
from typing import Optional, List

from aiogram import Bot
import aiogram.utils.markdown as fmt
from loguru import logger

from tg_bot.service.classes import FormatMessage

_BOT: Bot = Optional[None]
_CHANNELS: List[int] = Optional[None]
_MESSAGES_QUEUE: asyncio.Queue = Optional[None]


def format_message(data: dict) -> FormatMessage:
    date = fmt.hbold(datetime.datetime.now().strftime("%d-%m-%Y"))
    task_type = fmt.hbold('#Куплю\n' if data.get('type_task') == 'Купить' else '#Продам\n')
    fmt_body_list = list()
    fmt_body_list.append(fmt.text(f'Город: {data.get("city")}'))
    fmt_body_list.append(fmt.text(f'Тип оборудования/расходных материалов: {data.get("type_equipment_consumables")}'))
    fmt_body_list.append(fmt.text(f'Производитель: #{data.get("vendor")}'))
    fmt_body_list.append(fmt.text(f'Количество: {data.get("count")}'))
    fmt_body_list.append(fmt.text(f'Состояние: {data.get("condition")}'))
    fmt_body_list.append(fmt.text(f'Представитель: {data.get("salesman")}'))
    fmt_body_list.append(fmt.text(f'Цена: {data.get("price")} руб.'))
    fmt_body_list.append(fmt.text(f'Оплата: {data.get("payment_type")}'))
    if data.get("sending_to_another_city") != 'no_use':
        fmt_body_list.append(fmt.text(f'Отправка в другой город: {data.get("sending_to_another_city")}'))
    if data.get("email") != 'no_use':
        fmt_body_list.append(fmt.text(f'E-mail: {data.get("email")}'))
    fmt_body_list.append(fmt.text(f'Телефон: {data.get("phone")}'))
    fmt_body_list.append(fmt.text(f'Подробнее: {data.get("details")}'))

    fmt_body = fmt.text(*fmt_body_list, sep="\n")

    return FormatMessage(
        photo=None if data.get('photo') == 'no_use' else data.get('photo'),
        text=fmt.text(date, task_type, fmt_body, sep="\n")
    )


async def send_message(chat_id: int, data: dict, keyboard) -> bool:
    try:
        message = format_message(data=data)
        if message.photo is None:
            await _BOT.send_message(chat_id=chat_id,
                                    text=message.text,
                                    reply_markup=keyboard())
        else:
            await _BOT.send_photo(chat_id=chat_id,
                                  photo=message.photo,
                                  caption=message.text,
                                  reply_markup=keyboard())

        return True

    except Exception as error:
        logger.error(error)
        logger.error(traceback.format_exc(limit=None, chain=True))
        return False


async def send_message_to_channels(data: dict) -> bool:
    try:
        message = format_message(data=data)
        for id_channel in _CHANNELS:
            if message.photo is None:
                await _BOT.send_message(chat_id=id_channel,
                                        text=message.text)
            else:
                await _BOT.send_photo(chat_id=id_channel,
                                      photo=message.photo,
                                      caption=message.text)
        return True

    except Exception as error:
        logger.error(error)
        logger.error(traceback.format_exc(limit=None, chain=True))
        return False


def registry_mailing_service(bot: Bot, channels_ids: List[int]):
    global _BOT, _CHANNELS, _MESSAGES_QUEUE
    _BOT = bot
    _CHANNELS = channels_ids

    logger.info('Registry mailing service')
