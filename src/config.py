import logging
import sys
from configparser import ConfigParser
from os import path

_PROJECT_PATH: str = path.split(path.dirname(__file__))[0]
_MPLC4_LOG_DIR: str = "/opt/mplc4/log"
IGNORED_FILES: tuple = "start_log.txt"

config = ConfigParser()

try:
    config.read(f"{_PROJECT_PATH}/config.conf")

    logging_config = (
        logging.basicConfig(
            filename=(
                f"{_PROJECT_PATH}/cleaner.log"
                if config.getboolean("logging", "to_file")
                else None
            ),
            format="%(asctime)s:%(levelname)s:%(message)s",
            level={
                "info": logging.INFO,
                "warning": logging.WARNING,
                "error": logging.ERROR,
                "debug": logging.DEBUG,
            }.get(config["logging"]["level"].lower(), "debug"),
        )
        if config.getboolean("logging", "logging")
        else None
    )

    getint = lambda option: config.getint("defaults", option)

    MAX_DISK_USAGE: int = getint("max_disk_usage")
    MAX_LOGS_COUNT: int = getint("max_logs_count")
    INSPECTION_FREQUENCY: int = getint("inspection_frequency")

except Exception as error:
    logging.error(f' ошибка чтения конфига - "{error}", завершение работы..')
    sys.exit(1)
