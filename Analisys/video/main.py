from content.video import Video
from content.video_review import set_video_length
from content.video_review import get_videos_pages
from content.video_review import set_video_review
from content.video_watched_percent import set_watched_percent

from output.output import output

def Execute(cursor, _courseName):
    
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
    return output(videos, _courseName)
