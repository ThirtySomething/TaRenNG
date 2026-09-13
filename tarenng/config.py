import logging
import sys
from logging import Logger
from pathlib import Path
from venv import logger

from vendor.MDO import MDO

# import logging
# logger = logging.getLogger("mein_projekt.modul_a")


class Config(MDO):
    APP_NAME: str = "tarenng"

    def __init__(self) -> None:
        super().__init__(self.get_app_config(), True)
        self._logger: Logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        log_file: Path = self.get_app_dir() / f"{self.APP_NAME}.log"
        applogger: Logger = logging.getLogger(self.APP_NAME)
        if applogger.hasHandlers():
            return applogger
        applogger.setLevel(self.value_get("logging", "loglevel").upper())
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s:%(funcName)s | %(message)s", datefmt="%Y%m%d%H%M%S")
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        applogger.addHandler(file_handler)
        return applogger

    def get_app_config(self) -> Path:
        return self.get_app_dir() / f"{self.APP_NAME}.json"

    def get_app_dir(self) -> Path:
        if self.is_frozen():
            return Path(sys.executable).resolve().parent
        else:
            return Path(__file__).resolve().parent.parent

    def get_app_logger(self) -> Logger:
        return self._logger

    def is_frozen(self) -> bool:
        """Return whether the application is running from a PyInstaller bundle."""
        return bool(getattr(sys, "frozen", False))

    def setup(self) -> None:
        self.add("debug", "active", False)
        self.add("logging", "loglevel", "INFO")
        self.add("app", "collection_root", str(self.get_app_dir() / Path("collection")))
