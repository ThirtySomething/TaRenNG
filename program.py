import getpass
import logging
import platform
import sys
from zipfile import Path

from tarenng import Config, Defines, TaRenNG


################################################################################
def log_startup_info(config: Config) -> None:
    applogger: logging.Logger = config.get_app_logger()
    applogger.info(f"Operating system [{platform.uname()}]")
    applogger.info(f"Python version [{sys.version}]")
    applogger.info(f"User [{getpass.getuser()}] runs [{Defines.APP_NAME}] with the following settings:")
    applogger.info(f"Logger [{applogger.name}]")
    applogger.info(config)


################################################################################
if __name__ == "__main__":
    config: Config = Config()
    config_file: Path = config.get_app_config()
    if not config_file.exists() or not config.is_frozen():
        config.save()
    log_startup_info(config)
    program: TaRenNG = TaRenNG(config)
    program.process()
