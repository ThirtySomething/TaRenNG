import logging

from .episode_status import EpisodeStatus


class Episode:
    PREFIX: str = "Tatort"
    SUFFIX: str = "mp4"

    def __init__(self):
        self._logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")
        self._episodeid: int | None = None
        self._title: str | None = None
        self._commissioners: str | None = None
        self._case_number: int | None = None
        self._broadcast_station: str | None = None
        self._year: int | None = None
        self._status: EpisodeStatus = EpisodeStatus.ES_UNKNOWN

    def __eq__(self, other) -> bool:
        if not isinstance(other, Episode):
            return False

        result: bool = self._episodeid == other._episodeid
        result = result and (self._title == other._title)
        result = result and (self._commissioners == other._commissioners)
        result = result and (self._case_number == other._case_number)
        result = result and (self._broadcast_station == other._broadcast_station)
        result = result and (self._year == other._year)

        return result

    def __str__(self) -> str:
        # Tatort - 0001 - Taxi nach Leipzig - Trimmel - 1 - NDR - 1970.mp4
        return f"{Episode.PREFIX} - {self._episodeid:04d} - {self._title} - {self._commissioners} - {self._case_number} - {self._broadcast_station} - {self._year}.{Episode.SUFFIX}"

    def __repr__(self) -> str:
        return self.__str__()
