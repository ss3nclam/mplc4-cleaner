#!/usr/bin/python3

import logging
import os
from sys import exit
from time import sleep


MAX_LOGS_COUNT: int = 10
SLEEP_TIME: int = 3600  # ms
LOGS_DIR: str = '/opt/mplc4/log'

logging.basicConfig(filename=f'{LOGS_DIR}/cleaner_logs.txt', format='%(asctime)s:%(levelname)s: %(message)s', level=logging.DEBUG)


def get_logs_list() -> tuple:
    return tuple(filename for filename in os.listdir(LOGS_DIR) if 'mplc.core' in filename)


def main() -> None:
    try:
        logging.info(f'сканирование директории..')
        logs_before_cleaning = get_logs_list()
        
        if len(logs_before_cleaning) >= MAX_LOGS_COUNT:
            logging.info(f'превышен лимит логов, запуск очистки..')
            os.system(f'rm -rf {LOGS_DIR}/*mplc.core*')

            if logs_before_cleaning == get_logs_list():
                raise SystemError('очистка не произведена')
            
            else:
                logging.info(f'успешная очистка, перезапуск службы..')
                os.system('sudo systemctl restart mplc4')
                logging.info(f'служба перезапущена')

        else:
            logging.info(f'лимит логов не превышен')
    
    except Exception as error:
        logging.error(error)
        exit()
        

def scheduler(sleep_time: int = SLEEP_TIME):
    while True:
        main()
        logging.info(f'запуск сна..')
        sleep(sleep_time)

    
if __name__ == '__main__':
    scheduler()
