import logging
from logging import Logger
from pathlib import Path

from .config import Config
from .defines import Defines
from .episode_state import EpisodeState
from .fstool import FSTool
from .movie import Movie


class Statistics:
    ############################################################################
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")

    ############################################################################
    def process(self, collection_root: Path, episode_count: int) -> None:
        fstool: FSTool = FSTool(self._config)
        path_movies_seen: Path = collection_root / Defines.FOLDER_NAME_SEEN
        path_movies_unseen: Path = collection_root / Defines.FOLDER_NAME_UNSEEN
        movies_seen: list[Movie] = fstool.get_movies(path_movies_seen, EpisodeState.ES_SEEN)
        movies_unseen: list[Movie] = fstool.get_movies(path_movies_unseen, EpisodeState.ES_UNSEEN)
        episodes_seen: int = len(movies_seen)
        episodes_unseen: int = len(movies_unseen)
        episodes_own: int = episodes_seen + episodes_unseen
        self._logger.info(f"Total number of episodes [{episode_count:4d}]")
        self._logger.info(f"Own    [{episodes_own:4d} | {(100.0 / episode_count * episodes_own):6.2f}]")
        self._logger.info(f"Seen   [{episodes_seen:4d} | {(100.0 / episodes_own * episodes_seen):6.2f}]")
        self._logger.info(f"Unseen [{episodes_unseen:4d} | {(100.0 / episodes_own * episodes_unseen):6.2f}]")
