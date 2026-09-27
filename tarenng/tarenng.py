import logging
from logging import Logger
from pathlib import Path

from .collection import Collection
from .config import Config
from .statistics import Statistics
from .trash import Trash
from .webcache import WebCache


class TaRenNG:
    ############################################################################
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")
        self._collection: Collection = Collection(config)
        self._trash: Trash = Trash(config)
        self._statistics: Statistics = Statistics(config)

    ############################################################################
    def get_webcache(self) -> WebCache | None:
        webcache: WebCache = WebCache()
        cache_age: int = self._config.get_app_cache_age()
        cache_file: Path = self._config.get_app_cache_file()
        scraper_agent: str = self._config.get_app_scraper_agent()
        scraper_src: str = self._config.get_app_scraper_source()
        if not webcache.update(scraper_src, scraper_agent, cache_file, cache_age):
            return None
        return webcache

    ############################################################################
    def process(self) -> None:
        # Check the root folder of the collection
        collection_root: Path = self._config.get_app_collection_root()
        if not collection_root.exists():
            self._logger.error(f"Collection-root [{collection_root}] does not exist!")
            return
        # Ensure required folders for collection as well as ignore file
        if not self._collection.ensure_folders(collection_root):
            return
        # Get data from Wikipedia/cache
        cachedata: WebCache = self.get_webcache()
        if cachedata is None:
            self._logger.error("Webcache could not be updated, aborting!")
            return
        # Get raw data - the full cached data
        dataRaw: str = cachedata.get_data()
        self._logger.debug(f"Cached data: [{dataRaw[:300]}]...")
        # Build episode list from Wikipedia/cached page
        self._collection.initialize_list_episodes()
        if not self._collection.build_episode_list_from_html(dataRaw):
            self._logger.error(f"Cannot build episode list from cache data")
            return
        # Build list of already existing movies in seen/unseen folder
        self._collection.initialize_list_movies()
        if not self._collection.build_movie_list_from_folders(collection_root):
            self._logger.error(f"Cannot build movie list from folders")
            return
        # Because Wikipedia is the source of truth, maybe some files have to be renamed
        if not self._collection.fix_collection_naming(collection_root):
            self._logger.error(f"Failure during correcting names")
            return
        # If there are downloads available, process them
        if not self._collection.has_downloads(collection_root):
            self._logger.info(f"No downloads...")
        else:
            self._collection.rename_process(collection_root)
        max_age: int = self._config.get_app_trash_age()
        self._trash.cleanup(collection_root, max_age)
        episode_count: int = self._collection.get_number_of_episodes()
        self._statistics.process(collection_root, episode_count)
