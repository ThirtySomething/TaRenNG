import sys
from pathlib import Path

from vendor.MDO import MDO


class Config(MDO):
    APP_NAME: str = "tarenng"

    def __init__(self) -> None:
        super().__init__(self.get_app_config(), True)

    def get_app_config(self) -> Path:
        return self.get_app_dir() / f"{self.APP_NAME}.json"

    def get_app_dir(self) -> Path:
        if getattr(sys, "frozen", False):
            return Path(sys.executable).resolve().parent
        else:
            return Path(__file__).resolve().parent.parent

    def setup(self) -> None:
        self.add("debug", "active", False)
