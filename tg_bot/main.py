import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from loguru import logger
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

import tg_bot.service

from config import TgBot
from tg_bot import service
from tg_bot.filters.admin import AdminFilter
from tg_bot.handlers.echo import register_echo
from tg_bot.middlewares.environment import EnvironmentMiddleware

_messages_queue: asyncio.Queue = Optional[None]
_bot: Bot = Optional[None]
_dispatcher: Dispatcher = Optional[None]


def get_dispatcher() -> Dispatcher:
    return _dispatcher


def register_all_middlewares(dp: Dispatcher, config: TgBot):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp: Dispatcher):
    # register_admin(dp)
    # register_user(dp)
    register_echo(dp)


async def _on_startup(dp) -> None:
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("post_ad", 'Опубликовать объявление'),
        ],
        scope=types.BotCommandScopeDefault())
    pass


async def _on_shutdown(dp) -> None:
    await _dispatcher.storage.close()
    await _dispatcher.storage.wait_closed()


def main(config: TgBot):
    global _bot, _dispatcher, _messages_queue

    storage = MemoryStorage()
    # storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    _bot = Bot(token=config.token, parse_mode='HTML')
    _dispatcher = Dispatcher(_bot, storage=storage)

    register_all_middlewares(dp=_dispatcher, config=config)
    register_all_filters(dp=_dispatcher)
    # register_all_handlers(dp=_dispatcher)
    from tg_bot.handlers.user import register_user
    register_user(dp=_dispatcher)
    register_echo(dp=_dispatcher)
    service.registry_mailing_service(bot=_bot, channels_ids=config.channel_id)

    asyncio.set_event_loop(asyncio.new_event_loop())
    executor.start_polling(dispatcher=_dispatcher,
                           skip_updates=True,
                           on_startup=_on_startup,
                           on_shutdown=_on_shutdown)


def run(config: TgBot) -> None:
    logger.info('Starting bot')
    main(config=config)
