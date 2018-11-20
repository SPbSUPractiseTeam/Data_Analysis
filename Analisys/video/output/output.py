import json

def output(videos, courseName):
    """
    Write results of analysis to json file.
    :param videos:
    :param courseName:
    :return:
    """

    fileName = courseName + '_video_statistics.json'

    with open(fileName, "w") as out:
        courses = set()
        for video in videos:
            courses.add(video.course)
        courses_j = []
        for course_name in courses:
            sections = set()
            for video in videos:
                if video.course == course_name:
                    sections.add(video.section)

            course = dict()
            sections_j = []
            for section in sections:
                subsections = set()
                for video in videos:
                    if (video.course == course_name) and (video.section == section):
                        subsections.add(video.subsection)

                section_j = dict()
                subsections_j = []
                for subsection in subsections:
                    subsection_j = dict()
                    videos_j = []
                    for video in videos:
                        # todo: can be empty
                        if (video.course == course_name) and (video.section == section) and (video.subsection == subsection):
                            video_j = dict()
                            video_j["user_percent"] = video.user_percent
                            video_j["watched_percent"] = video.watched_percent
                            video_j["intervals_number"] = video.intervals_number
                            video_j["review_intervals"] = video.review_intervals
                            videos_j.append(video_j)
                    # todo: the sane with test
                    subsection_j["subsection_name"] = subsection
                    subsection_j["videos"] = videos_j
                    subsections_j.append(subsection_j)
                section_j["section_name"] = section
                section_j["subsections"] = subsections_j
                sections_j.append(section_j)
            course["course_name"] = course_name
            course["sections"] = sections_j
            courses_j.append(course)

        out.write(json.dumps(courses_j))
    return fileName
