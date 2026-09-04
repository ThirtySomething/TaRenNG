import getpass
import logging
import platform
import sys
from zipfile import Path

from tarenng import Config, TaRenNG

if __name__ == "__main__":
    config: Config = Config()
    config_file: Path = config.get_app_config()
    if not config_file.exists():
        config.save()
    applogger: logging.Logger = config.get_app_logger()
    applogger.info("Operating system: [%s]", platform.uname())
    applogger.info("Python version: [%s]", sys.version)
    applogger.info("User [%s] runs [%s] with the following settings:", getpass.getuser(), config.APP_NAME)
    applogger.info(config)
    program: TaRenNG = TaRenNG(config)
    program.process()
