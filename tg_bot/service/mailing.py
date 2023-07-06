import asyncio
import datetime
import traceback
from typing import Optional, List

from aiogram import Bot, types
import aiogram.utils.markdown as fmt
from aiogram.types import InputMediaPhoto, InputMedia
from loguru import logger

from tg_bot.service.classes import FormatMessage
from tg_bot.utils import point_deletion

_BOT: Bot = Optional[None]
_CHANNELS: List[int] = Optional[None]
_MESSAGES_QUEUE: asyncio.Queue = Optional[None]


def format_message(data: dict) -> FormatMessage:
    date = fmt.hbold(datetime.datetime.now().strftime("%d-%m-%Y"))

    tags_list = list()
    tags_list.append(fmt.hbold('#Куплю' if data.get('type_task') == 'Купить' else '#Продам'))
    tags_list.append(fmt.hbold(f'#{data.get("city").replace(" ", "_")}'))
    tags_list.append(fmt.hbold(f'#{data.get("type_equipment_consumables").replace(",", "").replace(" ", "_")}'))
    tags_list.append(fmt.hbold(f'#{data.get("vendor").replace(" ", "_")}'))

    fmt_body_list = list()
    fmt_body_list.append(fmt.text(f'Количество: {data.get("count")} шт.'))
    fmt_body_list.append(fmt.text(f'Состояние: {data.get("condition").lower()}.'))
    fmt_body_list.append(fmt.text(f'Представитель: {data.get("salesman").lower()}.'))
    fmt_body_list.append(fmt.text(f'Цена за единицу: {data.get("price")} руб.'))
    fmt_body_list.append(fmt.text(f'Оплата: {data.get("payment_type").lower()}.'))
    if data.get("sending_to_another_city") != 'no_use':
        fmt_body_list.append(fmt.text(f'Отправка в другой город: {data.get("sending_to_another_city").lower()}.'))
    if data.get("email") != 'no_use':
        fmt_body_list.append(fmt.text(f'Почта: {data.get("email").lower()}.'))
    fmt_body_list.append(fmt.text(f'Телефон: {data.get("phone")}.'))
    fmt_body_list.append(fmt.text(f'Подробнее: {data.get("details")}.'))

    fmt_header = fmt.text(*tags_list, sep="\n")
    fmt_body = fmt.text(*fmt_body_list, sep="\n")

    return FormatMessage(
        photo=None if data.get('photo') == 'no_use' else data.get('photo'),
        text=fmt.text(date, fmt_header, fmt_body, sep="\n\n")
    )


async def send_message(chat_id: int, data: dict, keyboard) -> bool:
    try:
        message = format_message(data=data)
        if message.photo is None:
            await _BOT.send_message(chat_id=chat_id,
                                    text=message.text,
                                    reply_markup=keyboard())
        else:

            media = types.MediaGroup()
            media.attach_photo(types.InputFile('1.jpg'), message.text)
            # media.attach_photo(types.InputFile('2.jpg'))
            # photo = InputMediaPhoto(media=media)
            await _BOT.send_media_group(chat_id=chat_id, media=media)
            # await _BOT.send_photo(chat_id=chat_id,
            #                       photo=message.photo,
            #                       caption=message.text,
            #                       reply_markup=keyboard())

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
