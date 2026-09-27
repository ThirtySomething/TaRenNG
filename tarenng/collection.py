import logging
from logging import Logger
from pathlib import Path

import bs4

from .config import Config
from .defines import Defines
from .episode import Episode
from .episode_list import EpisodeList
from .episode_state import EpisodeState
from .fstool import FSTool
from .movie import Movie
from .movie_list import MovieList
from .parser import Parser
from .trash import Trash


class Collection:
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._logger: Logger = logging.getLogger(f"{__package__}.{self.__class__.__name__}")
        self._episodelist: EpisodeList = EpisodeList(config)
        self._movielist: MovieList = MovieList(config)
        self._fstool: FSTool = FSTool(config)
        self._parser: Parser = Parser(config)
        self._trash: Trash = Trash(config)

    def ensure_folders(self, collection_root: Path) -> bool:
        # Check for existence of root folder
        if not collection_root.exists():
            return False
        # Ensure all required folders exists
        for folder in Defines.FOLDER_LIST_ALL:
            folder_path: Path = collection_root / folder
            if not self._fstool.ensure_folder(folder_path):
                self._logger.error(f"Collection-folder [{folder_path}] does not exist and cannot be created!")
                return False
        # Mark some folders with .ignore file to exclude from e. g. Jellyfin
        for ignore_folder in Defines.FOLDER_LIST_IGNORE:
            ignore_folder_file: Path = collection_root / ignore_folder / Defines.FILE_IGNORE
            ignore_folder_file.touch(exist_ok=True)
            if not ignore_folder_file.exists():
                self._logger.error(f"Collection-ignore-file [{ignore_folder_file}] does not exist and could not be created!")
                return False
        return True

    def build_episode_list_from_html(self, htmldata: str) -> bool:
        result: bool = False
        try:
            # Ensure empty episode list
            self._episodelist.list_initialize()
            # Get list of table rows of html page
            episodes_raw: list[bs4.element.Tag] = self._parser.get_episode_table_rows(htmldata)
            for episode_raw in episodes_raw:
                # Parse html table row to Episode
                episode: Episode | None = self._parser.get_episode_from_table_row(episode_raw)
                if episode is not None:
                    # Add episode
                    self._episodelist.list_element_add(episode)
            result = True
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def build_movie_list_from_folders(self, collection_root: Path) -> bool:
        result: bool = False
        try:
            for episode_state, folder_path in Defines.FOLDER_LIST_MOVIE.items():
                self._logger.debug(f"Working on folder [{folder_path}]")
                movielist: list[Movie] = self._fstool.get_episodes((collection_root / folder_path), episode_state)
                self._movielist.append(movielist)
            result = True
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def fix_collection_naming(self, collection_root: Path) -> bool:
        result: bool = False
        try:
            for movie in self._movielist.get_movie_list():
                if movie.get_episodestate() == EpisodeState.ES_TRASHED:
                    continue
                episode_from_movie: Episode = self._parser.get_episode_from_movie(movie)
                episodeid: int | None = episode_from_movie.get_episodeid()
                if episodeid is None:
                    self._logger.warning(f"Invalid episode number [{movie}]")
                    continue
                episode: Episode | None = self._episodelist.get_episode_by_id(episodeid)
                if episode is None:
                    self._logger.warning(f"Episode with number [{episode_from_movie._episodeid}] not found")
                    continue
                if not episode == episode_from_movie:
                    folder: Path = Defines.FOLDER_LIST_MOVIE[movie.get_episodestate()]
                    path_src: Path = collection_root / folder / movie.get_filename()
                    path_dst: Path = collection_root / folder / str(episode)
                    self._logger.info(f"rename [{path_src}] to [{path_dst}]")
                    path_src.rename(path_dst)
            result = True
        except Exception as ex:
            self._logger.exception(f"Exception: [{ex}]")
        return result

    def has_downloads(self, collection_root: Path) -> bool:
        folder2check: Path = collection_root / Defines.FOLDER_NAME_DOWNLOADS
        excludelist: list[str] = [Defines.FILE_IGNORE.name]
        result: bool = self._fstool.has_files_in_folder(folder2check, excludelist)
        return result

    def initialize_list_episodes(self) -> None:
        self._episodelist.list_initialize()

    def initialize_list_movies(self) -> None:
        self._movielist.list_initialize()

    def rename_process(self, collection_root: Path) -> None:
        downloads: list[Movie] = self._fstool.get_downloads(collection_root)
        for download in downloads:
            moviename: str = download.get_filename()
            episode: Episode | None = self._episodelist.get_episode_by_filename(moviename)
            if episode is None:
                self._logger.warning(f"No episode found for [{download}], ignoring")
                continue
            self._logger.debug(f"Found [{episode}] for [{download}]")
            # Rename downloaded file to new scheme
            path_src: Path = collection_root / Defines.FOLDER_NAME_DOWNLOADS / Path(moviename)
            path_dst: Path = collection_root / Defines.FOLDER_NAME_DOWNLOADS / str(episode)
            path_src.rename(path_dst)
            if not path_dst.exists():
                self._logger.error(f"Failure during rename of [{path_src}]")
                continue
            movie: Movie | None = self._movielist.get_movie_by_name(str(episode))
            path_src = collection_root / Defines.FOLDER_NAME_DOWNLOADS / str(episode)
            if movie is None:
                # Movie not in collection, move to unseen
                path_dst = collection_root / Defines.FOLDER_NAME_UNSEEN / str(episode)
                path_src.rename(path_dst)
                if not path_dst.exists():
                    self._logger.error(f"Failure during rename of [{path_src}]")
            else:
                if download.get_filesize() > movie.get_filesize():
                    path_dst: Path = collection_root / Defines.FOLDER_LIST_MOVIE[movie.get_episodestate()] / str(episode)
                    self._trash.trash(collection_root, movie)
                    path_src.rename(path_dst)
                    if not path_dst.exists():
                        self._logger.error(f"Failure during rename of [{path_src}]")
                else:
                    self._trash.trash(collection_root, download)
