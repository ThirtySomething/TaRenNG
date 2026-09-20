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

    def has_files_in_folder(self, folder: Path, files2ignore: list[str]) -> bool:
        tmp_list: list[Path] = []
        for current_entry in folder.iterdir():
            if current_entry.is_dir():
                continue
            if current_entry.name in files2ignore:
                continue
            tmp_list.append(current_entry)
        result: bool = 0 < len(tmp_list)
        return result
