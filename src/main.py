import logging

from .config import logging_config
from .modules.mplc4_logs_manager import MPLC4LogsManager
from .modules.scheduler import Scheduler
from .modules.system_service import SystemService


def main():

    scheduler = Scheduler()
    logs_manager = MPLC4LogsManager()

    @scheduler.job
    def manage_logs():
        if not logs_manager.is_limits_reached():
            logging.info(f"{logs_manager._logs_owner}: лимиты не превышены")
            return

        logging.info(f"{logs_manager._logs_owner}: лимиты превышены")
        logs_manager.remove("unused")

        if logs_manager.is_limits_reached():
            warning_msg: str = (
                "лимиты всё ещё превышены, будут удалены используемые файлы и перезапущена служба mplc4"
            )
            logging.warning(f"{logs_manager._logs_owner}: {warning_msg}")

            if logs_manager.remove("used"):
                mplc4_service = SystemService("mplc4")
                mplc4_service.restart()

            if mplc4_service.isactive() and not logs_manager.is_limits_reached():
                return

            elif not mplc4_service.isactive():
                logging.warning(
                    f"{logs_manager._logs_owner}: не удалось запустить службу mplc4"
                )

            elif logs_manager.is_limits_reached():
                logging.warning(
                    f"{logs_manager._logs_owner}: не удалось очистить физ. память доступными службе средствами"
                )

    scheduler.run()
