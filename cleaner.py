#!/bin/python3

from src import MPLC4LogFile, MPLC4LogsManager, System, SystemService, Scheduler
from src.config import logging_config

from src.main import scheduler


if __name__ == "__main__":
    scheduler.run()