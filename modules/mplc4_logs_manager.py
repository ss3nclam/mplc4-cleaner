import logging
import os
import sys

from ._settings import _MPLC4_LOG_DIR, MAX_LOGS_COUNT
from .mplc4_log_file import MPLC4LogFile
from .system import System


class MPLC4LogsManager:

    def __init__(self) -> None:
        self.__logs_owner: str = f'{self.__class__.__name__}'


    def get_logs(self, which: str) -> tuple:
        try:
            dir_content = tuple(
                MPLC4LogFile(filename) for filename in os.listdir(_MPLC4_LOG_DIR)
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


    def remove(self, which: str):
        try:
            files = tuple(logfile.name for logfile in self.get_logs(which))

            if not files:
                logging.info(f'{self.__logs_owner}: список запрашиваемых файлов ({which}) пуст')
                return

            logging.info(f'{self.__logs_owner}: удаление файлов ({which}): {files}..')

            file_names: str = ' '.join(f'{_MPLC4_LOG_DIR}/{file}' for file in files)

            cmd = f'sudo rm -rf {file_names}'
            shell = System.run_cmd(cmd)

            isremoved: bool = len(files) > len(self.get_logs(which))

            if not shell.stderr and isremoved:
                logging.info(f'{self.__logs_owner}: файлы успешно удалены')

            elif shell.stderr or not isremoved:
                shell_error: str = shell.stderr.strip('\n')
                error: str = shell_error if shell_error else 'файлы не были удалены'

                raise SystemError(f'неудачное выполнение команды - {error}')

        except Exception as exception:
            logging.error(f'{self.__logs_owner}: ошибка удаления файлов: {exception}')