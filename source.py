from preprocessing.logParser import openLogs

from content.video.video import Video
from content.video.video_review import set_video_length
from content.video.video_review import get_videos_pages
from content.video.video_review import set_video_review
from content.video.video_watched_percent import set_watched_percent

from output.output import output

if __name__ == '__main__':

    course_name = "spbu_ACADRU_spring_2018-TL"
    cursor = openLogs('logs/' + course_name)

    # Initialize videos
    pages = get_videos_pages(cursor)
    videos = []
    for page in pages:
        video = Video(page)
        videos.append(video)
    set_video_length(cursor, videos)
    set_video_review(cursor, videos)
    set_watched_percent(cursor, videos)

    # Output
    output(videos, course_name)