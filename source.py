import json

from preprocessing.logParser import openLogs

from content.video.video_review import get_video_review
from content.video.video_watched_percent import set_watched_percent

if __name__ == '__main__':

    cursor = openLogs('logs/spbu_ACADRU_spring_2018-TL')

    videos = get_video_review(cursor)
    set_watched_percent(cursor, videos)

    json.dumps()