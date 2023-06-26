import os
import sys
import traceback

from loguru import logger

from config import load_logging_config, LoggerConfig, load_config

import tg_bot


def configure_logger(logger_config: LoggerConfig) -> None:
    """
    Метод добавляет конфигурация для логгера.
    В качесте параметров используются значения из etc/logging.py возвращаемые функцией etc.config.get_logger_config
    :param logger_config: Конфигурация логгера
    :return: None
    """
    # setup_logging_handlers()
    logger.remove()

    logger.add(
        sink=sys.stderr,
        level=logger_config.logger_level
    )

    logger.add(
        sink=os.path.join(logger_config.logger_directory, logger_config.logger_filename),
        format=logger_config.logger_format,
        level=logger_config.logger_level,
        rotation=logger_config.logger_rotation,
        compression=logger_config.logger_compression
    )


if __name__ == '__main__':
    """
    Запуск программы
    """
    try:
        application_directory = os.path.dirname(__file__)

        # Конфигурирция логгера
        logging_config = load_logging_config(path=application_directory)
        configure_logger(logger_config=logging_config)

        # Запуск основной программы
        config = load_config()
        tg_bot.run(config=config)
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
    except Exception as ex:
        logger.error(ex)
        logger.error(traceback.format_exc(limit=None, chain=True))
