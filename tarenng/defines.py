from pathlib import Path

from .episode_state import EpisodeState


class Defines:
    APP_NAME: str = "tarenng"
    CACHE_AGE_DEFAULT: int = 6
    PATH_COLLECTION_ROOT: Path = Path("collection")

    FILE_IGNORE: Path = Path(".ignore")
    FOLDER_NAME_DOWNLOADS: Path = Path("downloads")
    FOLDER_NAME_SEEN: Path = Path("seen")
    FOLDER_NAME_TRASH: Path = Path(".trash")
    FOLDER_NAME_UNSEEN: Path = Path("unseen")

    FOLDER_LIST_ALL: list[Path] = [FOLDER_NAME_DOWNLOADS, FOLDER_NAME_SEEN, FOLDER_NAME_TRASH, FOLDER_NAME_UNSEEN]
    FOLDER_LIST_IGNORE: list[Path] = [FOLDER_NAME_DOWNLOADS, FOLDER_NAME_SEEN, FOLDER_NAME_TRASH]
    FOLDER_LIST_MOVIE: dict[EpisodeState, Path] = {
        EpisodeState.ES_SEEN: FOLDER_NAME_SEEN,
        EpisodeState.ES_UNSEEN: FOLDER_NAME_UNSEEN,
    }

    PREFIX: str = "Tatort"
    SUFFIX: str = "mp4"

    RE_REMARK: str = r"\((?!(?:Teil\s+1|Teil\s+2)\s*\))[^()]*\)"
    RE_GUEST_APPEARANCE: str = r"\s*\(Gastauftritt[^)]*\)"
    RE_CASE_NUMBER_SUFFIX: str = r"\s*(?:\(.*?\)|/.*)$"
    RE_YEAR: str = r"\b\d{4}\b"
    RE_EPISODE_ID_FROM_FILENAME: str = rf"^{PREFIX}\s*-\s*(?P<episodeid>\d+)\b"
    RE_EPISODE_FILENAME: str = (
        rf"^{PREFIX} - "
        r"(?P<episodeid>\d{4,}) - "
        r"(?P<title>.+) - "
        r"(?P<commissioners>[^-]+) - "
        r"(?P<case_number>\d+) - "
        r"(?P<broadcast_station>[^-]+) - "
        rf"(?P<year>\d{{4}})(?:_\d+)?\.{SUFFIX}$"
    )
    INVALID_REPLACEMENTS: list[tuple[str, str]] = [
        ("\u00a0", " "),  # Non breakable space
        ("\u2019", "'"),  # Typographical apostrophe
        ("\u2026", "..."),  # Horizontal ellipsis
        ("\u2013", "-"),  # En dash (longer dash)
        ("?", ""),  # Questionmark
        ("/", " "),  # Slash
        (":", " "),  # Colon
    ]

    URL_HASH_LENGTH: int = 8  # Length of MD5 hash used in cache filename
    SECONDS_PER_DAY: float = 86400.0  # Number of seconds in a day
