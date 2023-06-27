from typing import Optional, List

from aiogram import Bot
from loguru import logger

_BOT: Bot = Optional[None]
_CHANNELS: List[int] = Optional[None]


async def send_image_message(data: dict):
    for chat_id in _CHANNELS:
        _BOT.send_photo()


async def send_text_message(data: dict):
    for chat_id in _CHANNELS:
        _BOT.send_message()


def registry_mailing_service(bot: Bot, channels_ids: List[int]):
    global _BOT, _CHANNELS
    _BOT = bot
    _CHANNELS = channels_ids

    logger.info('Registry mailing service')
