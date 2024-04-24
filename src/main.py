from .system_service import SystemService
from .mplc4_logs_manager import MPLC4LogsManager
from .scheduler import Scheduler

scheduler = Scheduler()
logs_manager = MPLC4LogsManager()


@scheduler.job
def manage_logs():
    if not logs_manager.is_limits_reached():
        print('ok')
        return
    
    print('not ok')

    logs_manager.remove('unused')

    if logs_manager.is_limits_reached():
        print('not ok')
        logs_manager.remove('used')
        mplc4_service = SystemService('mplc4')
        mplc4_service.restart()

        if mplc4_service.isactive() and not logs_manager.is_limits_reached():
            print('good')
            return
