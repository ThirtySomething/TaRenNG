import logging
from logging import Logger

from .config import Config
from .episode import Episode


class EpisodeList:
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")
        self._episodes: list[Episode] = []

    def get_episode_by_filename(self, filename: str) -> Episode | None:
        if len(filename) >= 4 and filename[:4].isdigit():
            return self.get_episode_by_id(int(filename[:4]))

        result: Episode | None = None
        for current_episode in self._episodes:
            if current_episode.get_title().lower() in filename.lower():
                result = current_episode
                break
        return result

    def get_episode_by_id(self, id: int) -> Episode | None:
        result: Episode | None = None
        for current_episode in self._episodes:
            if id == current_episode.get_episodeid():
                result = current_episode
                break
        return result

    def get_episode_list(self) -> list[Episode]:
        return self._episodes

    def list_initialize(self) -> None:
        self._episodes = []

    def list_element_add(self, episode: Episode) -> None:
        for current_episode in self._episodes:
            if episode == current_episode:
                return

        self._episodes.append(episode)
        self._logger.debug(f"{episode}")
