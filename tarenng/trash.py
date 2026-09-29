import logging
import os
import time
from datetime import datetime, timedelta
from logging import Logger
from pathlib import Path

from .config import Config
from .defines import Defines
from .movie import Movie


class Trash:
    ############################################################################
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")

    ############################################################################
    def cleanup(self, collection_root: Path, trash_age: int) -> int:
        deleted: int = 0
        maxage: float = time.time() - trash_age * Defines.SECONDS_PER_DAY
        trashfolder: Path = collection_root / Defines.FOLDER_NAME_TRASH
        self._logger.info(
            "Delete files older than [%s] days from trash [%s]",
            trash_age,
            trashfolder,
        )
        # Loop over all in trash
        for trash_file in trashfolder.iterdir():
            if trash_file.is_file() and trash_file.name == Defines.FILE_IGNORE.name:
                # Skip file ".ignore"
                continue
            # Check only files
            if trash_file.is_file() and trash_file.stat().st_mtime < maxage:
                # Perform deletion
                os.remove(trash_file)
                self._logger.info(f"Delete file [{trash_file}]")
                deleted = deleted + 1
        return deleted

    ############################################################################
    def show_trash(self, collection_root: Path) -> None:
        trashfolder: Path = collection_root / Defines.FOLDER_NAME_TRASH
        self._logger.info(f"List files from trash [{trashfolder}]")
        today: datetime = datetime.today()
        # Loop over all in trash
        for trash_file in trashfolder.iterdir():
            filename: str = trash_file.name
            # Check only files
            if trash_file.is_file():
                # Ignore marker for media servers
                if trash_file.name == Defines.FILE_IGNORE.name:
                    continue
                # List file
                file_mod_time: datetime = datetime.fromtimestamp(trash_file.stat().st_mtime)
                age: timedelta = today - file_mod_time
                self._logger.info(f"File [{filename}|{age.days:02d}]")

    ############################################################################
    def trash(self, collection_root: Path, movie: Movie | None) -> bool:
        result: bool = False
        if movie is None:
            return result
        for suffix in range(1, 11):
            filename: Path = Path(movie.get_filename())
            path_dst: Path = collection_root / Defines.FOLDER_NAME_TRASH / Path(f"{filename.stem}_{suffix:02d}.{Defines.SUFFIX}")
            if not path_dst.exists():
                collection_folder: Path = Defines.FOLDER_NAME_DOWNLOADS
                if movie.get_episodestate() in Defines.FOLDER_LIST_MOVIE:
                    collection_folder = Defines.FOLDER_LIST_MOVIE[movie.get_episodestate()]
                path_src: Path = collection_root / collection_folder / filename
                self._logger.info(f"Trashing [{path_src}]")
                path_src.rename(path_dst)
                now: float = time.time()
                self._logger.debug(f"Set access/modified timestamp of [{path_dst}]")
                os.utime(path_dst, (now, now))
                result = True
                break
        return result
