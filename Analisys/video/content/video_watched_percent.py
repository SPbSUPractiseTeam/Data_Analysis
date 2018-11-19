from dateutil import parser
import pandas as pd

from .video import Video


def get_user_ids(cursor):
    users = set()
    request = """
                select distinct user_id
                from load_video            
                """
    cursor.execute(request)
    data = cursor.fetchall()
    for i in range(len(data)):
        users.add(data[i][0])
    return users

def get_skipped_length(cursor, video, user_id):
    """
    For video and user return length of video that was skipped.
    """

    # video intervals with length less then min_length will ignore
    min_length = 1

    request = """
                select video_time, null as video_old_time, null as video_new_time, execute_time
                from play_video
                where page = "{0}"
                and user_id = {1}
                """.format(video.page, user_id)
    cursor.execute(request)
    data = cursor.fetchall()
    columns_names = []
    for i in cursor.description[:]:
        columns_names.append(i[0])
    play_df = pd.DataFrame(data=data, columns=columns_names)
    play_df = play_df.join(pd.DataFrame({'event': ["play_video"] * len(data)}))

    request = """
                select video_time, null as video_old_time, null as video_new_time, execute_time
                from pause_video
                where page = "{0}"
                and user_id = {1}
                """.format(video.page, user_id)
    cursor.execute(request)
    data = cursor.fetchall()
    columns_names = []
    for i in cursor.description[:]:
        columns_names.append(i[0])
    pause_df = pd.DataFrame(data=data, columns=columns_names)
    pause_df = pause_df.join(pd.DataFrame({'event': ["pause_video"] * len(data)}))

    request = """
                select video_time, null as video_old_time, null as video_new_time, execute_time
                from stop_video
                where page = "{0}"
                and user_id = {1}
                """.format(video.page, user_id)
    cursor.execute(request)
    data = cursor.fetchall()
    columns_names = []
    for i in cursor.description[:]:
        columns_names.append(i[0])
    stop_df = pd.DataFrame(data=data, columns=columns_names)
    stop_df = stop_df.join(pd.DataFrame({'event': ["stop_video"] * len(data)}))

    request = """
                select null as video_time, video_old_time, video_new_time, execute_time
                from seek_video
                where page = "{0}"
                and user_id = {1}
                """.format(video.page, user_id)
    cursor.execute(request)
    data = cursor.fetchall()
    columns_names = []
    for i in cursor.description[:]:
        columns_names.append(i[0])
    seek_df = pd.DataFrame(data=data, columns=columns_names)
    seek_df = seek_df.join(pd.DataFrame({'event': ["seek_video"] * len(data)}))

    df = pd.concat([play_df, pause_df, stop_df, seek_df], axis=0)
    df.execute_time = [parser.parse(x) for x in df.execute_time.values]
    df = df.sort_values(by=["execute_time"])

    not_watched = [(0, video.length)]
    begin = None
    for event in df.iterrows():
        event = event[1]
        if event.event == "play_video":
            begin = event.video_time
        else:
            if event.event == "seek_video":
                end = event.video_old_time
            else:
                end = event.video_time

            if begin == None:
                continue

            new_interv = []
            for interval in not_watched:
                if not ((interval[0] > end) or (interval[1] < begin)):
                    # [] - interval
                    # () - begin, end

                    # [...()...]
                    if (interval[0] < begin) and (interval[1] > end):
                        if (begin - interval[0]) > min_length:
                            new_interv.append((interval[0], begin))
                        if (interval[1] - end) > min_length:
                            new_interv.append((end, interval[1]))

                    # [...( ] )
                    elif (interval[0] < begin) and (interval[1] < end):
                        if (begin - interval[0]) > min_length:
                            new_interv.append((interval[0], begin))

                    # ( [ )...]
                    elif (interval[0] > begin) and (interval[1] > end):
                        if (interval[1] - end) > min_length:
                            new_interv.append((end, interval[1]))

                    # ( [ ] ) - don't add anything

                    not_watched.remove(interval)
            if new_interv:
                not_watched = not_watched + new_interv
            begin = None

    length = 0.0
    for interval in not_watched:
        length += interval[1] - interval[0]
    return length

def set_watched_percent(cursor, videos):
    user_ids = get_user_ids(cursor=cursor)

    for video in videos:
        request = """
                    select distinct user_id
                    from play_video
                    where page = "{}"
                    """.format(video.page)
        cursor.execute(request)
        data = cursor.fetchall()
        video.set_user_percent(len(data) / len(user_ids))

        watched_users = set()
        for i in range(len(data)):
            watched_users.add(data[i][0])

        skip_length = 0.0
        user_quantity = len(watched_users)
        for user_id in watched_users:
            skip_length += get_skipped_length(cursor=cursor,  video=video, user_id=user_id)
        video.set_watched_percent(1 - skip_length / (video.length * user_quantity))
