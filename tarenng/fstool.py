import logging
from logging import Logger
from pathlib import Path

from .config import Config
from .defines import Defines
from .episode_state import EpisodeState
from .movie import Movie


class FSTool:
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")

    def ensure_folder(self, folder: Path) -> bool:
        if not folder.exists():
            self._logger.debug(f"Creating folder [{folder}]")
            folder.mkdir(parents=True, exist_ok=True)
        return folder.exists() and folder.is_dir()

    def get_downloads(self, collection_root: Path) -> list[Movie]:
        result: list[Movie] = []
        path_downloads: Path = collection_root / Defines.FOLDER_NAME_DOWNLOADS
        if not path_downloads.exists():
            self._logger.error(f"Downloadpath [{path_downloads}] does not exist")
            return result
        for entry in path_downloads.iterdir():
            if entry.is_dir():
                continue
            if entry.name == Defines.FILE_IGNORE.name:
                continue
            movie: Movie = Movie(entry, EpisodeState.ES_DOWNLOADED)
            result.append(movie)
        self._logger.debug(f"{result}")
        return result

    def get_episodes(self, folder: Path, episodestate: EpisodeState) -> list[Movie]:
        result: list[Movie] = []
        for data in folder.iterdir():
            if data.is_dir():
                self._logger.debug(f"Skip folder [{data}] in [{folder}]")
                continue
            if not (data.name.startswith(Defines.PREFIX) and data.name.endswith(Defines.SUFFIX)):
                self._logger.debug(f"Ignore [{data}]")
                continue
            movie: Movie = Movie(data, episodestate)
            self._logger.debug(f"Movie [{movie}]")
            result.append(movie)
        return result

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
