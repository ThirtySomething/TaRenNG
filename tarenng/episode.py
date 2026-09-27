import logging
from logging import Logger

from .defines import Defines


class Episode:
    ############################################################################
    def __init__(self):
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")
        self._episodeid: int | None = None
        self._title: str | None = None
        self._commissioners: str | None = None
        self._case_number: int | None = None
        self._broadcast_station: str | None = None
        self._year: int | None = None

    ############################################################################
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

    ############################################################################
    def __repr__(self) -> str:
        return self.__str__()

    ############################################################################
    def __str__(self) -> str:
        return f"{Defines.PREFIX} - {self._episodeid:04d} - {self._title} - {self._commissioners} - {self._case_number} - {self._broadcast_station} - {self._year}.{Defines.SUFFIX}"

    ############################################################################
    def get_broadcast_station(self) -> str | None:
        return self._broadcast_station

    ############################################################################
    def set_broadcast_station(self, broadcast_station: str | None) -> None:
        self._broadcast_station = broadcast_station

    ############################################################################
    def get_case_number(self) -> int | None:
        return self._case_number

    ############################################################################
    def set_case_number(self, case_number: int | None) -> None:
        self._case_number = case_number

    ############################################################################
    def get_commissioners(self) -> str | None:
        return self._commissioners

    ############################################################################
    def set_commissioners(self, commissioners: str | None) -> None:
        self._commissioners = commissioners

    ############################################################################
    def get_episodeid(self) -> int | None:
        return self._episodeid

    ############################################################################
    def set_episodeid(self, episodeid: int | None) -> None:
        self._episodeid = episodeid

    ############################################################################
    def get_title(self) -> str | None:
        return self._title

    ############################################################################
    def set_title(self, title: str | None) -> None:
        self._title = title

    ############################################################################
    def get_year(self) -> int | None:
        return self._year

    ############################################################################
    def set_year(self, year: int | None) -> None:
        self._year = year
