import logging
import re
from logging import Logger

import bs4
from bs4 import BeautifulSoup

from .config import Config
from .defines import Defines
from .episode import Episode
from .movie import Movie


class Parser:
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")

    def _get_table_column_by_number(self, tablerow: bs4.element.Tag, number: int) -> str:
        cells: list[bs4.element.Tag] = tablerow.find_all("td")
        result = cells[number].get_text().strip()
        return result

    def _get_broadcast_station(self, tablerow: bs4.element.Tag) -> str | None:
        result: str | None = None
        try:
            result = self._get_table_column_by_number(tablerow, 2)
            for original, replacement in Defines.INVALID_REPLACEMENTS:
                result = result.replace(original, replacement)
            result = result.strip()
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def _get_case_number(self, tablerow: bs4.element.Tag) -> int | None:
        result: int | None = None
        try:
            casenumber: str | None = self._get_table_column_by_number(tablerow, 5)
            casenumber = re.sub(Defines.RE_CASE_NUMBER_SUFFIX, "", casenumber)
            result = int(casenumber)
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def _get_commissioners(self, tablerow: bs4.element.Tag) -> str | None:
        result: str | None = None
        try:
            result = self._get_table_column_by_number(tablerow, 4)
            result = re.sub(Defines.RE_GUEST_APPEARANCE, "", result).strip()
            for original, replacement in Defines.INVALID_REPLACEMENTS:
                result = result.replace(original, replacement)
            result = result.strip()
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def _get_episodeid(self, tablerow: bs4.element.Tag) -> int | None:
        result: int | None = None
        try:
            result = int(self._get_table_column_by_number(tablerow, 0))
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def _get_title(self, tablerow: bs4.element.Tag) -> str | None:
        result: str | None = None
        try:
            result = self._get_table_column_by_number(tablerow, 1)
            result = re.sub(Defines.RE_REMARK, "", result).strip()
            for original, replacement in Defines.INVALID_REPLACEMENTS:
                result = result.replace(original, replacement)
            result = result.strip()
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def _get_year(self, tablerow: bs4.element.Tag) -> int | None:
        result: int | None = None
        try:
            date_value: str = self._get_table_column_by_number(tablerow, 3)
            year_match: re.Match[str] | None = re.search(Defines.RE_YEAR, date_value)
            if year_match is not None:
                result = int(year_match.group())
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def get_episode_table_rows(self, htmldata: str) -> list[bs4.element.Tag]:
        result: list[bs4.element.Tag] = []
        try:
            parser: BeautifulSoup = BeautifulSoup(htmldata, "html.parser")
            for tablerow in parser.find("table", class_="wikitable").find_all("tr"):
                if tablerow.find("th") is not None:
                    continue
                result.append(tablerow)
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def get_episode_from_table_row(self, tablerow: bs4.element.Tag) -> Episode | None:
        result: Episode = Episode()

        result.set_episodeid(self._get_episodeid(tablerow))
        result.set_title(self._get_title(tablerow))
        result.set_commissioners(self._get_commissioners(tablerow))
        result.set_case_number(self._get_case_number(tablerow))
        result.set_broadcast_station(self._get_broadcast_station(tablerow))
        result.set_year(self._get_year(tablerow))

        return result

    def get_episode_from_movie(self, movie: Movie) -> Episode:
        result: Episode = Episode()
        movie_match: re.Match[str] | None = re.fullmatch(Defines.RE_EPISODE_FILENAME, movie.get_filename())
        if movie_match is not None:
            episodeid: int | None = int(movie_match.group("episodeid"))
            title: str | None = movie_match.group("title")
            commissioners: str | None = movie_match.group("commissioners").strip()
            case_number: int | None = int(movie_match.group("case_number"))
            broadcast_station: str | None = movie_match.group("broadcast_station").strip()
            year: int | None = int(movie_match.group("year"))
            result.set_episodeid(episodeid)
            result.set_title(title)
            result.set_commissioners(commissioners)
            result.set_case_number(case_number)
            result.set_broadcast_station(broadcast_station)
            result.set_year(year)
            return result

        episode_id_match: re.Match[str] | None = re.match(
            Defines.RE_EPISODE_ID_FROM_FILENAME,
            movie.get_filename(),
        )
        if episode_id_match is not None:
            result.set_episodeid(int(episode_id_match.group("episodeid")))

        self._logger.warning(f"Partially parsed movie filename [{movie._filename}]")
        return result
