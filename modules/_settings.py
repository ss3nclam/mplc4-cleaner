from configparser import ConfigParser
import logging
import os
import sys


project_path: str = os.path.dirname(__file__).rstrip(f'{__name__}/')

config = ConfigParser()

try:
    config.read(f'{project_path}/config.conf')

    logging_config = logging.basicConfig(
        filename = f'{project_path}/logs.txt' if config.getboolean('app', 'logfile') else None,
        format = '%(asctime)s:%(levelname)s:%(message)s',
        level = {
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'DEBUG': logging.DEBUG,
            }.get(config['app']['loging_level'], 'DEBUG')
        )
    
    MAX_DISK_USAGE: int = config.getint('app', 'max_disk_usage')
    MAX_LOGS_COUNT: int = config.getint('app', 'max_logs_count')
    INSPECTION_FREQUENCY: int = config.getint('app', 'inspection_frequency')

    _MPLC4_LOG_DIR: str = '/opt/mplc4/log'
    _IGNORED_FILES: tuple = (
        'start_log.txt'
    )

except Exception as error:
    logging.error(' ошибка чтения конфига, выключение..')
    sys.exit(1)
