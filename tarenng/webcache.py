import hashlib
import logging
import time
from logging import Logger
from pathlib import Path

import requests

from .defines import Defines


class WebCache:
    ############################################################################
    def __init__(self) -> None:
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")
        self._data: str | None = None

    ############################################################################
    def _calculate_cache_age_in_days(self, cache_file: Path) -> int:
        cache_age_in_seconds: float = time.time() - cache_file.stat().st_mtime
        return int(cache_age_in_seconds / Defines.SECONDS_PER_DAY)

    ############################################################################
    def _get_cache_file_name(self, url_src: str, cache_file: Path) -> Path:
        url_hash: str = hashlib.md5(url_src.encode()).hexdigest()[: Defines.URL_HASH_LENGTH]
        cache_stem: str = cache_file.stem
        cache_filename: str = f"{cache_stem}_{url_hash}.html"
        return cache_file.parent / cache_filename

    ############################################################################
    def _is_cache_valid(self, cache_file: Path, max_age: int) -> bool:
        if not cache_file.exists():
            self._logger.debug(f"Cache-file [{cache_file}] does not exist.")
            return False
        cache_age_in_days = self._calculate_cache_age_in_days(cache_file)
        if cache_age_in_days <= max_age:
            self._set_cache_data(cache_file)
            return True
        self._logger.debug(f"Cache-file [{cache_file}] is outdated ({cache_age_in_days} > {max_age} days).")
        return False

    ############################################################################
    def _set_cache_data(self, cache_file: Path) -> None:
        self._data = cache_file.read_text(encoding="utf-8")

    ############################################################################
    def _update_cache_file(self, url_src: str, agent: str, cache_file: Path) -> bool:
        headers = {"User-Agent": agent}
        try:
            response = requests.get(url_src, headers=headers)
            response.raise_for_status()
            cache_file.write_text(response.text, encoding="utf-8")
            self._set_cache_data(cache_file)
            self._logger.info(f"Cache-file [{cache_file}] updated successfully.")
        except requests.RequestException as ex:
            self._logger.error(f"Failed to update cache-file [{cache_file}]: {ex}")
            return False
        return True

    ############################################################################
    def get_data(self) -> str | None:
        return self._data

    ############################################################################
    def update(self, url_src: str, agent: str, cache_file_raw: Path, max_age: int) -> bool:
        cache_file: Path = self._get_cache_file_name(url_src, cache_file_raw)
        if self._is_cache_valid(cache_file, max_age):
            return True
        return self._update_cache_file(url_src, agent, cache_file)
