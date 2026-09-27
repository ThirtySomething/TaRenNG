import logging
import sys
from logging import Logger
from pathlib import Path
from venv import logger

from vendor.MDO import MDO

from .defines import Defines


class Config(MDO):

    def __init__(self) -> None:
        super().__init__(self.get_app_config(), True)
        self._logger: Logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        log_file: Path = self.get_app_dir() / f"{Defines.APP_NAME}.log"
        applogger: Logger = logging.getLogger(__package__)
        if applogger.hasHandlers():
            return applogger
        applogger.setLevel(self.get_logging_loglevel())
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s:%(lineno)s:%(funcName)s | %(message)s", datefmt="%Y%m%d%H%M%S")
        file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        file_handler.setFormatter(formatter)
        applogger.addHandler(file_handler)
        return applogger

    def get_app_cache_age(self) -> int:
        age: int = Defines.CACHE_AGE_DEFAULT
        age_raw = self.value_get("app", "cache_age")
        if isinstance(age_raw, int):
            age = age_raw
        else:
            try:
                age = int(age_raw)
            except (ValueError, TypeError):
                self._logger.warning(f"Invalid cache_age value [{age_raw}] configured, using default value [{Defines.CACHE_AGE_DEFAULT}].")
        return age

    def get_app_cache_file(self) -> Path:
        return Path(self.value_get("app", "cache_file"))

    def get_app_collection_root(self) -> Path:
        return Path(self.value_get("app", "collection_root"))

    def get_app_config(self) -> Path:
        return self.get_app_dir() / f"{Defines.APP_NAME}.json"

    def get_app_dir(self) -> Path:
        if self.is_frozen():
            return Path(sys.executable).resolve().parent
        else:
            return Path(__file__).resolve().parent.parent

    def get_app_logger(self) -> Logger:
        return self._logger

    def get_app_scraper_agent(self) -> str:
        return str(self.value_get("app", "scraper_agent"))

    def get_app_scraper_source(self) -> str:
        return str(self.value_get("app", "scraper_source"))

    def get_app_trash_age(self) -> int:
        age: int = Defines.TRASH_AGE_DEFAULT
        age_raw = self.value_get("app", "trash_age")
        if isinstance(age_raw, int):
            age = age_raw
        else:
            try:
                age = int(age_raw)
            except (ValueError, TypeError):
                self._logger.warning(f"Invalid trash_age value [{age_raw}] configured, using default value [{Defines.TRASH_AGE_DEFAULT}].")
        return age

    def get_logging_loglevel(self) -> str:
        return self.value_get("logging", "loglevel").upper()

    def is_frozen(self) -> bool:
        """Return whether the application is running from a PyInstaller bundle."""
        return bool(getattr(sys, "frozen", False))

    def setup(self) -> None:
        self.add("app", "cache_age", Defines.CACHE_AGE_DEFAULT)
        self.add("app", "cache_file", str(self.get_app_dir() / Defines.PATH_COLLECTION_ROOT / f"{Defines.APP_NAME}.html"))
        self.add("app", "collection_root", str(self.get_app_dir() / Defines.PATH_COLLECTION_ROOT))
        self.add("app", "scraper_agent", "TaRenNG/0.0 (https://github.com/ThirtySomething/TaRenNG/) generic-library/0.0")
        self.add("app", "scraper_source", "https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen")
        self.add("app", "trash_age", Defines.TRASH_AGE_DEFAULT)
        self.add("logging", "loglevel", "info")
