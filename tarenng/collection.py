import logging
from pathlib import Path

from .config import Config
from .fstool import FSTool


class Collection:
    FILE_IGNORE: Path = Path(".ignore")
    FOLDER_NAME_DOWNLOADS: Path = Path("downloads")
    FOLDER_NAME_SEEN: Path = Path("seen")
    FOLDER_NAME_TRASH: Path = Path(".trash")
    FOLDER_NAME_UNSEEN: Path = Path("unseen")

    FOLDER_LIST_ALL: list[Path] = [FOLDER_NAME_DOWNLOADS, FOLDER_NAME_SEEN, FOLDER_NAME_TRASH, FOLDER_NAME_UNSEEN]
    FOLDER_LIST_IGNORE: list[Path] = [FOLDER_NAME_DOWNLOADS, FOLDER_NAME_SEEN, FOLDER_NAME_TRASH]

    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self.logger = logging.getLogger(f"{self._config.APP_NAME}.{self.__class__.__name__}")

    def ensure_folders(self) -> bool:
        collection_root: Path = Path(self._config.value_get("app", "collection_root"))
        fsTool: FSTool = FSTool(self._config)
        if not collection_root.exists():
            self.logger.error(f"Collection-root [{collection_root}] does not exist!")
            return False

        for folder in Collection.FOLDER_LIST_ALL:
            folder_path: Path = collection_root / folder
            if not fsTool.ensure_folder(folder_path):
                self.logger.error(f"Collection-folder [{folder_path}] does not exist and could not be created!")
                return False

        for ignore_folder in Collection.FOLDER_LIST_IGNORE:
            ignore_folder_file: Path = collection_root / ignore_folder / Collection.FILE_IGNORE
            ignore_folder_file.touch(exist_ok=True)
            if not ignore_folder_file.exists():
                self.logger.error(f"Collection-ignore-file [{ignore_folder_file}] does not exist and could not be created!")
                return False

        return True
