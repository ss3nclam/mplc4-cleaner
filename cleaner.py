import os

# from modules import SystemService
# from modules import MPLC4LogFile
from modules import MPLC4LogsManager, System
from modules._settings import logging_config


# mplc4 = SystemService('mplc4')
# mplc4.restart()
# print(mplc4.isactive())


logs_manager = MPLC4LogsManager()

print(logs_manager.get_logs('used'))
print(System.get_diskspace_usage())
logs_manager.remove('unused')
print(System.get_diskspace_usage())
