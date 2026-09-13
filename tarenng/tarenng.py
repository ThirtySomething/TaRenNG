import logging
from pathlib import Path

from .collection import Collection
from .config import Config
from .webcache import WebCache


class TaRenNG:
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self.logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")
        self._collection: Collection = Collection(self._config)

    def get_webcache(self) -> WebCache | None:
        webcache: WebCache = WebCache()
        cache_age: int = self._config.get_cache_age()
        cache_file: Path = self._config.get_cache_file()
        scraper_agent: str = self._config.get_scraper_agent()
        scraper_src: str = self._config.get_scraper_source()
        if not webcache.update(scraper_src, scraper_agent, cache_file, cache_age):
            return None
        return webcache

    def process(self) -> None:
        if not self._collection.ensure_folders():
            return

        if self.get_webcache() is None:
            self.logger.error("Webcache could not be updated, aborting!")
            return
