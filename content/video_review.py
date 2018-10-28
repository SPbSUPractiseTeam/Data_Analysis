from content.video import Video
import pandas as pd
import numpy as np

def get_videos_pages(cursor):
    """get the set of pages y load_video event"""

    request = """
            select *
            from load_video
            """
    cursor.execute(request)
    data = cursor.fetchall()

    columns_names = []
    for i in cursor.description[:]:
        columns_names.append(i[0])

    df = pd.DataFrame(data=data, columns=columns_names)

    pages = set()
    for page in df.page:
        pages.add(page)
    return pages

def get_video_review(cursor):
    videos = []
    for page in get_videos_pages(cursor):
        # get length by stop_video event
        request = """
                select max(video_time)
                from stop_video
                where page = "{}"
                """.format(page)
        cursor.execute(request)
        length = cursor.fetchall()[0]
        length = length[0]
        if length == None:
            # todo: make handler
            pass
        else:

            # todo: intervals_number
            intervals_number = 50
            review_intervals = np.zeros(shape=(intervals_number,))
            step = length / intervals_number

            request = """
                    select video_old_time, video_new_time
                    from seek_video
                    where page = "{}"
                    """.format(page)
            cursor.execute(request)
            for video_old_time, video_new_time in cursor.fetchall():
                begin = int(video_new_time / step)
                end = int(video_old_time / step) + 1
                for i in range(begin, end):
                    review_intervals[i] += 1

            video = Video(page, length, intervals_number, review_intervals)
            videos.append(video)
    return videos