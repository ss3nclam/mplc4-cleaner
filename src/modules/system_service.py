import logging
import sys

from .system import System


class SystemService(object):

    def __init__(self, name: str) -> None:
        self.__service_name: str = name
        self.__logs_owner: str = f'{self.__class__.__name__}:{self.__service_name}'


    def isactive(self) -> bool:
        cmd: str = f'sudo systemctl is-active {self.__service_name}'
        shell = System.run_cmd(cmd)

        try:
            if not shell.returncode:
                return shell.stdout.rstrip('\n') == 'active'

        except Exception:
            shell_error: str = shell.stderr.strip('\n')
            logging.error(f'{self.__logs_owner}: ошибка проверки статуса: {shell_error}')
            sys.exit(1)


    def start(self) -> None:
        if not self.isactive():
            logging.info(f'{self.__logs_owner}: запуск..')
            cmd: str = f'sudo systemctl start {self.__service_name}'
            shell = System.run_cmd(cmd)

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
            shell = System.run_cmd(cmd)

            try:
                if self.isactive():
                    logging.info(f'{self.__logs_owner}: успешно перезапущена')

                else:
                    shell_error: str = shell.stderr.strip('\n')
                    logging.warning(f'{self.__logs_owner}: не удалось перезапустить - "{shell_error}", попытка принудительного запуска..')

                    self.start()

                    if not self.isactive():
                        raise SystemError(f'не удалось перезапустить и принудительно запустить')

            except Exception as error:
                logging.error(f'{self.__logs_owner}: ошибка перезапуска: {error}')
                sys.exit(1)

        else:
            logging.warning(f'{self.__logs_owner}: неактивна')
            self.start()
