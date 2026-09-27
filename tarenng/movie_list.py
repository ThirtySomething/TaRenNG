from .config import Config
from .movie import Movie


class MovieList:
    ############################################################################
    def __init__(self, config: Config) -> None:
        self._config: Config = config
        self._movies: list[Movie] = []

    ############################################################################
    def append(self, data: list[Movie]) -> None:
        if isinstance(data, list):
            for cur_element in data:
                if isinstance(cur_element, Movie):
                    self._movies.append(cur_element)

    ############################################################################
    def get_movie_by_name(self, moviename: str) -> Movie | None:
        result: Movie | None = None
        for movie in self._movies:
            if moviename == movie.get_filename():
                result = movie
                break
        return result

    ############################################################################
    def get_movie_list(self) -> list[Movie]:
        return self._movies

    ############################################################################
    def list_initialize(self) -> None:
        self._movies = []
