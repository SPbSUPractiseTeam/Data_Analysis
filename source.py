from preprocessing.logParser import openLogs

if __name__ == '__main__':
    cursor = openLogs('logs/spbu_ACADRU_spring_2018-TL')

    request = """
        select *
        from play_video
    """

    cursor.execute(request)
    raw = cursor.fetchone()
    print(raw)