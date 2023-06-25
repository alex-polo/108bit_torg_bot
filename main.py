import asyncio
from typing import Optional

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import TgBot
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from loguru import logger


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    # register_admin(dp)
    register_user(dp)

    register_echo(dp)


dp: Dispatcher = Optional[None]


async def main(config: TgBot):
    # storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    storage = MemoryStorage()
    bot = Bot(token=config.token, parse_mode='HTML')
    global dp
    dp = Dispatcher(bot, storage=storage)

    # bot['config'] = config

    register_all_middlewares(dp, config)
    # register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await dp.start_polling()
    finally:
        # await dp.storage.close()
        # await dp.storage.wait_closed()
        await bot.session.close()


def run(config: TgBot) -> None:
    logger.info('Starting bot')
    asyncio.run(main(config=config))

# if __name__ == '__main__':
#     try:
#         asyncio.run(main())
#     except (KeyboardInterrupt, SystemExit):
#         logger.error("Bot stopped!")
