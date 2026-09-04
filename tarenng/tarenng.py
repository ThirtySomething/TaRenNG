from .config import Config


class TaRenNG:
    def __init__(self, config: Config) -> None:
        self._config: Config = config

    def process(self) -> None:
        print(f"Hello world from [{self.__class__.__name__}]!")
