import logging
import os
import sys
from configparser import ConfigParser


PROJECT_PATH: str = os.path.dirname(__file__).rstrip(f'{__name__}/')

config = ConfigParser()

try:
    config.read(f'{PROJECT_PATH}/config.conf')

    logging_config = logging.basicConfig(
        filename = f'{PROJECT_PATH}/logs.txt' if config.getboolean('app', 'logfile') else None,
        format = '%(asctime)s:%(levelname)s:%(message)s',
        level = {
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'debug': logging.DEBUG,
            }.get(config['app']['loging_level'].lower(), 'debug')
        )
    
    MAX_DISK_USAGE: int = config.getint('app', 'max_disk_usage')
    MAX_LOGS_COUNT: int = config.getint('app', 'max_logs_count')
    INSPECTION_FREQUENCY: int = config.getint('app', 'inspection_frequency')
    MPLC4_LOG_DIR: str = '/opt/mplc4/log'
    IGNORED_FILES: tuple = (
        'start_log.txt'
    )

except Exception as error:
    logging.error(f' ошибка чтения конфига - "{error}", завершение работы..')
    sys.exit(1)
