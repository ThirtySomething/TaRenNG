import logging

from .collection import Collection
from .config import Config


class TaRenNG:
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self.logger = logging.getLogger(f"{self._config.APP_NAME}.{self.__class__.__name__}")
        self._collection: Collection = Collection(self._config)

    def process(self) -> None:
        if not self._collection.ensure_folders():
            return
