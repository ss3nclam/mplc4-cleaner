#!/usr/bin/python3

import cmd
import logging
import os
import subprocess
import sys


MAX_LOGS_COUNT: int = 10
MAX_DIR_SIZE: float = 10.0 # TODO Написать метод проверки лимита занимаемой памяти
SLEEP_TIME: int = 1800  # sec

_CLEANER_SCRIPT_FILENAME: str = __file__.split('/')[-1]
_CLEANER_LOGS_FILENAME: str = 'cleaner_logs.txt'

_MPLC4_LOGS_DIR: str = '/opt/mplc4/log'
_IGNORED_FILES: tuple = (
    _CLEANER_SCRIPT_FILENAME,
    _CLEANER_LOGS_FILENAME,
    'start_log.txt'
)


logging.basicConfig(
    # filename = f'{_MPLC4_LOGS_DIR}/{_CLEANER_LOGS_FILENAME}', # FIXME Логи скрипта в файл отключены
    format = '%(asctime)s:%(levelname)s:%(message)s',
    level = logging.DEBUG
    )


def run_cmd(command: str):
    return subprocess.run(
        args = command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True,
        text = True
        )


class SystemService(object):

    def __init__(self, name: str) -> None:
        self.__service_name: str = name
        self.__logs_owner: str = f'{self.__class__.__name__}:{self.__service_name}'


    def isactive(self) -> bool:
        cmd: str = f'sudo systemctl is-active {self.__service_name}'
        shell = run_cmd(cmd)

        try:
            if not shell.returncode:
                return shell.stdout.strip('\n') == 'active'

        except Exception:
            shell_error: str = shell.stderr.strip('\n')
            logging.error(f'{self.__logs_owner}: ошибка проверки статуса: {shell_error}')
            sys.exit(1)


    def start(self) -> None:
        if not self.isactive():
            logging.info(f'{self.__logs_owner}: запуск..')
            cmd: str = f'sudo systemctl start {self.__service_name}'
            shell = run_cmd(cmd)

            try:
                if self.isactive():
                    logging.info(f'{self.__logs_owner}: успешно запущена')
                
                else:
                    shell_error: str = shell.stderr.strip('\n')
                    raise SystemError(f'неудачное выполнение команды - {shell_error}')
                
            except Exception as error:
                logging.error(f'{self.__logs_owner}: ошибка запуска: {error}')
                sys.exit(1)

        else:
            logging.warning(f'{self.__logs_owner}: уже запущена')


    def stop(self):
        # TODO Написать метод для остановки службы
        pass


    def restart(self):
        if self.isactive():
            logging.info(f'{self.__logs_owner}: перезапуск..')
            cmd: str = f'sudo systemctl restart {self.__service_name}'
            shell = run_cmd(cmd)

            try:
                if self.isactive():
                    logging.info(f'{self.__logs_owner}: успешно перезапущена')
                
                else:
                    shell_error: str = shell.stderr.strip('\n')
                    raise SystemError(f'неудачное выполнение команды - {shell_error}')
                
            except Exception as error:
                logging.error(f'{self.__logs_owner}: ошибка перезапуска: {error}')
                sys.exit(1)

        else:
            logging.warning(f'{self.__logs_owner}: неактивна')
            self.start()


class MPLC4LogFile(object):

    def __init__(self, filename) -> None:
        self.name = filename
        self.__logs_owner: str = f'{self.__class__.__name__}:{self.name}'


    def isused(self) -> bool:
        cmd: str = f'sudo lsof {_MPLC4_LOGS_DIR}/{self.name}'
        shell = run_cmd(cmd)

        try:
            if not shell.stdout and shell.stderr:
                shell_error = shell.stderr.strip('\n')
                raise SystemError(f'не удалось проверить статус использования файла - {shell_error}')
            
            else:
                return shell.stdout != ''

        except Exception as error:
            logging.error(f'{self.__logs_owner}: ошибка проверки статуса: {error}')
            sys.exit(1)


    def isignored(self) -> bool:
        return self.name in _IGNORED_FILES


class MPLC4LogsManager:

    def __init__(self) -> None:
        self.__logs_owner: str = f'{self.__class__.__name__}'

    
    def get_logs(self, which: str) -> tuple:
        try:
            dir_content = tuple(
                MPLC4LogFile(filename) for filename in os.listdir(_MPLC4_LOGS_DIR)
                )
            logs = tuple(file for file in dir_content if not file.isignored())
            
            if which == 'used':
                usage_filter = lambda x: x.isused()

            elif which == 'unused':
                usage_filter = lambda x: not x.isused()

            elif which == 'all':
                usage_filter = lambda _: True

            else:
                raise SyntaxError(f'передан неподдерживаемый аргумент функции - {which}')

            return tuple(logfile for logfile in logs if usage_filter(logfile))
            
        except Exception as error:
            logging.error(f'{self.__logs_owner}: ошибка получения списка файлов: {error}')
            sys.exit(1)
    

    def is_limits_reached(self) -> bool:
        # TODO Добавить проверку лимита занимаемой физ. памяти
        return len(self.get_logs()) >= MAX_LOGS_COUNT


    def remove_logs(self, which: str):
        try:
            files = tuple(logfile.name for logfile in self.get_logs(which))

            if not files:
                logging.info(f'{self.__logs_owner}: список запрашиваемых файлов пуст')
                return

            logging.info(f'{self.__logs_owner}: удаление файлов {files}..')

            file_names: str = ' '.join(f'{_MPLC4_LOGS_DIR}/{file}' for file in files)

            cmd = f'sudo rm -rf {file_names}'
            shell = run_cmd(cmd)

            isremoved: bool = len(files) > len(self.get_logs(which))

            if not shell.stderr and isremoved:
                logging.info(f'{self.__logs_owner}: файлы успешно удалены')

            elif shell.stderr or not isremoved:
                shell_error: str = shell.stderr.strip('\n')
                error: str = shell_error if shell_error else 'файлы не были удалены'

                raise SystemError(f'неудачное выполнение команды - {error}')

        except Exception as exception:
            logging.error(f'{self.__logs_owner}: ошибка удаления файлов: {exception}')
