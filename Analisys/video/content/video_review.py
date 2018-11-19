import pandas as pd

from .video import Video

def get_videos_pages(cursor):
    """
    Get the set of pages by load_video event
    :param cursor:
    :return:
    """

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

def set_video_length(cursor, videos):
    """
    Set video length for iterable videos object
    :param cursor:
    :param videos:
    :return:
    """
    for video in videos:
        request = """
                select max(video_time)
                from stop_video
                where page = "{}"
                """.format(video.page)
        cursor.execute(request)
        length = cursor.fetchall()[0]
        video.set_length(length[0])
        if length == None:
            # todo: make handler
            pass

def set_video_review(cursor, videos):
    """
    Set list of numbers - how many times users watched video again
    :param cursor:
    :return:
    """

    # get length by stop_video event
    for video in videos:
        # todo: intervals_number
        intervals_number = 50
        review_intervals = [0] * intervals_number
        step = video.length / intervals_number

        request = """
                select video_old_time, video_new_time
                from seek_video
                where page = "{}"
                """.format(video.page)
        cursor.execute(request)
        for video_old_time, video_new_time in cursor.fetchall():
            begin = int(video_new_time / step)
            end = int(video_old_time / step) + 1
            for i in range(begin, end):
                review_intervals[i] += 1

        video.set_review(intervals_number, review_intervals)
