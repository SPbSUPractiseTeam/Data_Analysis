class Video:
    def __init__(self, page):
        """
        Initialize by page of video
        :param page:
        """
        self.page = page
        arr = page.split("/")
        # todo: exception handler
        if arr[arr.index("courseware") - 1] != "":
            self.course = arr[arr.index("courseware") - 1]
        if arr[arr.index("courseware") + 1] != "":
            self.section = arr[arr.index("courseware") + 1]
        if arr[arr.index("courseware") + 2] != "":
            self.subsection = arr[arr.index("courseware") + 2]

    def set_length(self, length):
        """
        Set video length
        :param length:
        :return:
        """
        self.length = length

    def set_review(self, intervals_number, review_intervals):
        """
        Set number of intervals of video and iterable object with values how many times
        users watched interval again
        :param intervals_number:
        :param review_intervals:
        :return:
        """
        self.intervals_number = intervals_number
        self.review_intervals = review_intervals

    def set_user_percent(self, percent):
        """
        Set percent of users who watched video
        :param percent:
        :return:
        """
        self.user_percent = percent

    def set_watched_percent(self, watched_percent):
        """
        Setting mean percent of video that was watched by users
        :param watched_percent:
        :return:
        """
        self.watched_percent = watched_percent