import os.path
from dataclasses import dataclass
from typing import List

from environs import Env

######################################################################################################
#                                   Настройки логирования
######################################################################################################
logger_directory = 'logs'
logger_filename = 'bot.log'
logger_format = '{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | file:{file} | line:{line} - {message} ", level="ERROR'
logger_level = 'DEBUG'
logger_rotation = '500 MB'
logger_compression = 'zip'
debug_sqlalchemy = False


@dataclass
class LoggerConfig:
    logger_directory: str
    logger_filename: str
    logger_format: str
    logger_level: str
    logger_rotation: str
    logger_compression: str


@dataclass
class TgBot:
    bot_name: str
    token: str
    channel_id: List[int]
    admin_ids: List[int]


def load_logging_config(path: str) -> LoggerConfig:
    return LoggerConfig(
        logger_directory=os.path.join(path, logger_directory),
        logger_filename=logger_filename,
        logger_format=logger_format,
        logger_level=logger_level,
        logger_rotation=logger_rotation,
        logger_compression=logger_compression
    )


def load_config(path: str = None) -> TgBot:
    env = Env()
    env.read_env(path)

    return TgBot(
        bot_name=env.str("BOT_NAME"),
        token=env.str("BOT_TOKEN"),
        channel_id=list(map(int, env.list("CHANNEL_IDS"))),
        admin_ids=list(map(int, env.list("ADMIN_IDS"))),
    )
