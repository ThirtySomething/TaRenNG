import logging
from pathlib import Path

from .config import Config


class FSTool:
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")

    def ensure_folder(self, folder: Path) -> bool:
        if not folder.exists():
            self._logger.debug(f"Creating folder [{folder}]")
            folder.mkdir(parents=True, exist_ok=True)
        return folder.exists() and folder.is_dir()
