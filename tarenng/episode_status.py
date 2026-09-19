from enum import Enum


class EpisodeStatus(Enum):
    ES_UNKNOWN = 0
    ES_DOWNLOADED = 1
    ES_UNSEEN = 2
    ES_SEEN = 3
    ES_TRASHED = 4
