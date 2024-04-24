import logging
import sys

from .config import IGNORED_FILES, _MPLC4_LOG_DIR
from .system import System


class MPLC4LogFile(object):

    def __init__(self, filename) -> None:
        self.name = filename
        self.__logs_owner: str = f'{self.__class__.__name__}:{self.name}'


    def __repr__(self) -> str:
        return self.name


    def isused(self) -> bool:
        cmd: str = f'sudo lsof {_MPLC4_LOG_DIR}/{self.name}'
        shell = System.run_cmd(cmd)

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
        return self.name in IGNORED_FILES