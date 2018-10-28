class Video:
    def __init__(self, page, length, intervals_number, review_intervals):
        self.page = page
        self.length = length
        self.intervals_number = intervals_number
        self.review_intervals = review_intervals

    def set_user_percent(self, percent):
        self.user_percent = percent

    def set_watched_percent(self, watched_percent):
        self.watched_percent = watched_percent