import logging
import os
import subprocess
import sys


MAX_LOGS_COUNT: int = 10
SLEEP_TIME: int = 3600  # s
_LOGS_DIR: str = '/opt/mplc4/log'

logging.basicConfig(
    filename = f'{_LOGS_DIR}/cleaner_logs.txt',
    format = '%(asctime)s:%(levelname)s:%(message)s',
    level = logging.DEBUG
    )


def run_cmd(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args = command,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        shell = True,
        text = True
        )


class SystemService(object):

    def __init__(self, name: str) -> None:
        self.__name: str = name
        self.__logs_owner: str = f'{self.__class__.__name__}:{self.name}'


    def isactive(self) -> bool:
        cmd: str = f'sudo systemctl is-active {self.name}'
        shell: subprocess.CompletedProcess[str] = run_cmd(cmd)

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
            cmd: str = f'sudo systemctl start {self.name}'
            shell: subprocess.CompletedProcess[str] = run_cmd(cmd)

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
            cmd: str = f'sudo systemctl restart {self.name}'
            shell: subprocess.CompletedProcess[str] = run_cmd(cmd)

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
        self.__filename = filename


    def isused(self):
        # TODO Написать метод, проверяющий используется ли файл
        pass


class LogsAssistaint:
    
    def __init__(self) -> None:
        self.__logs_tuple = \
        tuple(filename for filename in os.listdir(_LOGS_DIR) if 'mplc.core' in filename)

