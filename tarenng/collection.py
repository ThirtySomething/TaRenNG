import logging
from pathlib import Path

import bs4

from .config import Config
from .episode import Episode
from .episode_list import EpisodeList
from .fstool import FSTool
from .parser import Parser


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
        self._episodelist: EpisodeList = EpisodeList(config)
        self._fsTool: FSTool = FSTool(config)
        self._logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")

    def ensure_folders(self) -> bool:
        collection_root: Path = self._config.get_app_collection_root()
        if not collection_root.exists():
            self._logger.error(f"Collection-root [{collection_root}] does not exist!")
            return False
        for folder in Collection.FOLDER_LIST_ALL:
            folder_path: Path = collection_root / folder
            if not self._fsTool.ensure_folder(folder_path):
                self._logger.error(f"Collection-folder [{folder_path}] does not exist and could not be created!")
                return False
        for ignore_folder in Collection.FOLDER_LIST_IGNORE:
            ignore_folder_file: Path = collection_root / ignore_folder / Collection.FILE_IGNORE
            ignore_folder_file.touch(exist_ok=True)
            if not ignore_folder_file.exists():
                self._logger.error(f"Collection-ignore-file [{ignore_folder_file}] does not exist and could not be created!")
                return False
        return True

    def build_episode_list_from_cache(self, dataraw: str) -> bool:
        result: bool = False
        try:
            parser: Parser = Parser(self._config)
            self._episodelist.list_initialize()
            episodes_raw: list[bs4.element.Tag] = parser.get_episode_data_raw(dataraw)
            for episode_raw in episodes_raw:
                episode: Episode | None = parser.get_episode_data(episode_raw)
                if episode is not None:
                    self._episodelist.list_element_add(episode)
            result = True
        except Exception as ex:
            self._logger.exception(f"Failure: [{ex}]")
        return result

    def has_downloads(self) -> bool:
        collection_root: Path = self._config.get_app_collection_root()
        folder2check: Path = collection_root / Collection.FOLDER_NAME_DOWNLOADS
        excludelist: list[str] = [Collection.FILE_IGNORE.name]
        result: bool = self._fsTool.has_files_in_folder(folder2check, excludelist)
        return result
