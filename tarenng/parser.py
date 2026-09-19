import logging
import re

import bs4
from bs4 import BeautifulSoup

from .config import Config
from .episode import Episode


class Parser:
    RE_REMARK: str = r"\((?!(?:Teil\s+1|Teil\s+2)\s*\))[^()]*\)"
    RE_GUEST_APPEARANCE: str = r"\s*\(Gastauftritt[^)]*\)"
    RE_CASE_NUMBER_SUFFIX: str = r"\s*(?:\(.*?\)|/.*)$"
    RE_YEAR: str = r"\b\d{4}\b"
    INVALID_REPLACEMENTS: list[tuple[str, str]] = [
        ("\u00a0", " "),
        ("\u2019", "'"),
        ("\u2026", "..."),
        ("\u2013", "-"),
        ("?", ""),
        (" /", " - "),
    ]

    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")

    def _get_episode_broadcast_station(self, dataraw: bs4.element.Tag) -> str | None:
        result: str | None = None
        try:
            cells: list[bs4.element.Tag] = dataraw.find_all("td")
            result = cells[2].get_text()
            for original, replacement in Parser.INVALID_REPLACEMENTS:
                result = result.replace(original, replacement)
        except Exception as ex:
            self._logger.exception(f"Exception parsing commissioners: [{ex}]")
        return result

    def _get_episode_case_number(self, dataraw: bs4.element.Tag) -> int | None:
        result: int | None = None
        try:
            cells: list[bs4.element.Tag] = dataraw.find_all("td")
            result = cells[5].get_text()
            result = re.sub(Parser.RE_CASE_NUMBER_SUFFIX, "", result)
            result = int(result.strip())
        except Exception as ex:
            self._logger.exception(f"Exception parsing episode id: [{ex}]")
        return result

    def _get_episode_commissioners(self, dataraw: bs4.element.Tag) -> str | None:
        result: str | None = None
        try:
            cells: list[bs4.element.Tag] = dataraw.find_all("td")
            result = cells[4].get_text()
            result = re.sub(Parser.RE_GUEST_APPEARANCE, "", result).strip()
            for original, replacement in Parser.INVALID_REPLACEMENTS:
                result = result.replace(original, replacement)
        except Exception as ex:
            self._logger.exception(f"Exception parsing commissioners: [{ex}]")
        return result

    def _get_episode_id(self, dataraw: bs4.element.Tag) -> int | None:
        result: int | None = None
        try:
            cells: list[bs4.element.Tag] = dataraw.find_all("td")
            result = cells[0].get_text()
            result = int(result.strip())
        except Exception as ex:
            self._logger.exception(f"Exception parsing episode id: [{ex}]")
        return result

    def _get_episode_title(self, dataraw: bs4.element.Tag) -> str | None:
        result: str | None = None
        try:
            cells: list[bs4.element.Tag] = dataraw.find_all("td")
            result = cells[1].get_text()
            result = result.strip()
            result = re.sub(Parser.RE_REMARK, "", result).strip()
            for original, replacement in Parser.INVALID_REPLACEMENTS:
                result = result.replace(original, replacement)
            result = result.strip()
        except Exception as ex:
            self._logger.exception(f"Exception parsing title: [{ex}]")
        return result

    def _get_episode_year(self, dataraw: bs4.element.Tag) -> int | None:
        result: int | None = None
        try:
            cells: list[bs4.element.Tag] = dataraw.find_all("td")
            date_value: str = cells[3].get_text()
            year_match: re.Match[str] | None = re.search(Parser.RE_YEAR, date_value)
            if year_match is not None:
                result = int(year_match.group())
        except Exception as ex:
            self._logger.exception(f"Exception parsing episode year: [{ex}]")
        return result

    def get_episode_data(self, dataraw: bs4.element.Tag) -> Episode | None:
        result: Episode = Episode()

        result._episodeid = self._get_episode_id(dataraw)
        result._title = self._get_episode_title(dataraw)
        result._commissioners = self._get_episode_commissioners(dataraw)
        result._case_number = self._get_episode_case_number(dataraw)
        result._broadcast_station = self._get_episode_broadcast_station(dataraw)
        result._year = self._get_episode_year(dataraw)

        self._logger.debug(f"Episode [{result}]")

        # self._year: int | None = None
        # self._status: EpisodeStatus = EpisodeStatus.ES_UNKNOWN

        return result

    def get_episode_data_raw(self, dataraw: str) -> list[bs4.element.Tag]:
        result: list[bs4.element.Tag] = []
        try:
            parser: BeautifulSoup = BeautifulSoup(dataraw, "html.parser")
            for tablerow in parser.find("table", class_="wikitable").find_all("tr"):
                if tablerow.find("th") is not None:
                    continue
                result.append(tablerow)
        except Exception as ex:
            self._logger.exception(f"Exception while parsing: [{ex}]")
        return result
