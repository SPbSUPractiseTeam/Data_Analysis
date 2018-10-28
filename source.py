from preprocessing.logParser import openLogs
import matplotlib.pyplot as plt
import numpy as np

from content.video_review import get_video_review
from content.video_watched_percent import set_watched_percent

if __name__ == '__main__':

    cursor = openLogs('logs/spbu_ACADRU_spring_2018-TL')

    videos = get_video_review(cursor)
    video = videos[8]
    plt.plot(np.linspace(0, video.length, video.intervals_number), video.review_intervals)
    #plt.show()

    set_watched_percent(cursor, videos)

    for i in videos:
        print(i.watched_percent)