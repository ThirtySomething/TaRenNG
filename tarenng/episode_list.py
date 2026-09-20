import logging

from .config import Config
from .episode import Episode


class EpisodeList:
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")
        self._episodes: list[Episode] = []

    def get_episode_list(self) -> list[Episode]:
        return self._episodes

    def list_initialize(self) -> None:
        self._episodes: list[Episode] = []

    def list_element_add(self, episode: Episode) -> None:
        found: bool = False
        for current_episode in self._episodes:
            if episode == current_episode:
                found = True
                break

        if not found:
            self._episodes.append(episode)
            self._logger.debug(f"{episode}")
