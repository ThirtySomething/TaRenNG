from pathlib import Path

from .episode_state import EpisodeState


class Movie:
    def __init__(self, data_raw: Path, episode_state: EpisodeState):
        self._filename: str = data_raw.name
        self._filesize: int = data_raw.stat().st_size
        self._state: EpisodeState = episode_state

    def __str__(self) -> str:
        return f"{self._state.name} - {self._filesize:010d}: {self._filename}"

    def __repr__(self) -> str:
        return self.__str__()

    def get_filename(self) -> str:
        return self._filename

    def get_filesize(self) -> int:
        return self._filesize

    def get_episodestate(self) -> EpisodeState:
        return self._state
