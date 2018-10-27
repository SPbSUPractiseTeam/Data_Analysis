import json
import sqlite3
from pprint import pprint

def openLogs(inpFileName):#convert logs into database returns cursor, needed for requests
    skip_str = "skip_this"
    no_extra_str = "no_extra"
    def getCommonInfo(data):
        res = str(data["context"]["user_id"]) +",'"+ data["context"]["course_id"] + "','" + data["time"]+"'"
        return res;
    
    def writeToDb(cursor, extraInfo = no_extra_str):
        res = getCommonInfo(data)
        res += ",'" + data["page"] + "'" + extra_info;
        write_to_database = "insert into " + event_type + " values (" + res + ");"
        cursor.execute(write_to_database)


    databaseName = inpFileName + ".sqlite"
    inpfile = open(inpFileName)
    #try:
    database = sqlite3.connect(databaseName)
    cursor = database.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS load_video;
        CREATE TABLE load_video 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS pause_video;
        CREATE TABLE pause_video 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,video_time real
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS play_video;
        CREATE TABLE play_video 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,video_time real
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS stop_video;
        CREATE TABLE stop_video 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,video_time real
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS seek_video;
        CREATE TABLE seek_video 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,video_old_time real
            ,video_new_time real
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS speed_change_video;
        CREATE TABLE speed_change_video 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,video_time real
            ,speed_old real
            ,speed_new real
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS hide_transcript;
        CREATE TABLE hide_transcript 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,video_time real
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS show_transcript;
        CREATE TABLE show_transcript 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,video_time real
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS video_hide_cc_menu;
        CREATE TABLE video_hide_cc_menu 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS video_show_cc_menu;
        CREATE TABLE video_show_cc_menu 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS problem_check;
        CREATE TABLE problem_check 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,questions varchar(2000)
            ,grade real
            ,max_grade real
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS problem_show;
        CREATE TABLE problem_show 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
        )
    """)
    cursor.executescript("""
        DROP TABLE IF EXISTS problem_hint;
        CREATE TABLE problem_hint 
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,page varchar(300)
            ,hint_number int
        )
    """)
    video_events = ["hide_transcript", "edx.video.transcript.hidden","load_video", "edx.video.loaded", "pause_video", "edx.video.paused", "play_video", "edx.video.played", "seek_video", "edx.video.position.changed", "show_transcript", "edx.video.transcript.shown", "speed_change_video", "stop_video", "edx.video.stopped", "video_hide_cc_menu", "video_show_cc_menu"];
    problem_events = ["edx.problem.hint.demandhint_displayed", "edx.problem.hint.feedback_displayed", "problem_check", "problem_check_fail", "problem_graded", "problem_rescore", "problem_rescore_fail", "problem_reset", "problem_save", "problem_show", "reset_problem", "reset_problem_fail", "save_problem_fail", "save_problem_success", "showanswer"];
    special_exam_events = ["edx.special_exam.proctored.attempt.created", "edx.special_exam.practice.attempt.created", "edx.special_exam.timed.attempt.created", "edx.special_exam.proctored.attempt.declined", "edx.special_exam.proctored.attempt.deleted", "edx.special_exam.practice.attempt.deleted", "edx.special_exam.timed.attempt.deleted", "edx.special_exam.proctored.attempt.download_software_clicked", "edx.special_exam.practice.attempt.download_software_clicked", "edx.special_exam.proctored.attempt.error", "edx.special_exam.practice.attempt.error", "edx.special_exam.proctored.attempt.ready_to_start", "edx.special_exam.practice.attempt.ready_to_start", "edx.special_exam.proctored.attempt.ready_to_submit", "edx.special_exam.practice.attempt.ready_to_submit", "edx.special_exam.timed.attempt.ready_to_submit", "edx.special_exam.proctored.attempt.rejected", "edx.special_exam.proctored.attempt.review_received", "edx.special_exam.proctored.attempt.started", "edx.special_exam.practice.attempt.started", "edx.special_exam.timed.attempt.started", "edx.special_exam.proctored.attempt.submitted", "edx.special_exam.practice.attempt.submitted", "edx.special_exam.timed.attempt.submitted", "edx.special_exam.proctored.attempt.verified", "edx.special_exam.proctored.option-presented"];
    for line in inpfile:
        data = json.loads(line);
        if (data["event_type"] in video_events + ["mobile"]):
            if data["event_type"] == "mobile":
                event_type = data["name"]
            else: 
                event_type = data["event_type"]

            extra_info = ""
            event = json.loads(data["event"])
            if event_type in ["hide_transcript", "edx.video.transcript.hidden"]:
                event_type = "hide_transcript"
                extra_info = ", " + str(event["currentTime"])

            elif event_type in ["show_transcript", "edx.video.transcript.shown"]:
                event_type = "show_transcript"
                extra_info = ", " + str(event["currentTime"])

            elif event_type in ["load_video", "edx.video.loaded"]:
                event_type = "load_video"
                
            elif event_type in ["pause_video", "edx.video.paused"]:
                event_type = "pause_video"
                extra_info = ", " + str(event["currentTime"])

            elif event_type in ["play_video", "edx.video.played"]:
                event_type = "play_video"
                extra_info = ", " + str(event["currentTime"])

            elif event_type in ["stop_video", "edx.video.stopped"]:
                event_type = "stop_video"
                extra_info = ", " + str(event["currentTime"])

            elif event_type in ["seek_video", "edx.video.position.changed"]:
                event_type = "seek_video"
                extra_info = ", " + str(event["old_time"]) + "," + str(event["new_time"])

            elif event_type == "speed_change_video":
                extra_info = ", " + str(event["current_time"]) + "," + str(event["old_speed"]) + "," + str(event["new_speed"])

            else:
                extra_info = skip_str

            if extra_info != skip_str:
               extra_info += "\n"
               writeToDb(cursor, extra_info)

        elif data["event_type"] in problem_events:
            event_type = data["event_type"]
            extra_info = ""
            event =data["event"]
            problem_id = ""

            if event_type == "edx.problem.hint.demandhint_displayed":
                extra_info = str(event["hint_index"])
                problem_id = event["module_id"] 

            elif event_type == "edx.problem.hint.feedback_displayed":
                extra_info = skip_str

            elif event_type == "problem_check":
                if data["event_source"] == "server":
                    extra_info += ", '{  "
                    for key in event["submission"]:
                        extra_info += '"' + key + '"' + ":" + str(event["submission"][key]["correct"]) + ", "
                    extra_info = extra_info[0:-2]
                    extra_info += "}', " + str(event["grade"]) + ", " + str(event["max_grade"])
                    problem_id = event["problem_id"]

                else:
                    extra_info = skip_str

            elif event_type == "problem_check_fail":
                extra_info = skip_str

            elif event_type == "problem_graded":
                extra_info = skip_str

            elif event_type == "problem_rescore":
                #extra_info = str(event["orig_score"]) + ", " + str(event["new_score"])
                extra_info = skip_str

            elif event_type == "problem_rescore_fail":
                extra_info = skip_str

            elif event_type == "problem_reset":
                extra_info = skip_str

            elif event_type == "problem_save":
                extra_info = skip_str

            elif event_type == "problem_show":
                event = json.loads(data["event"])
                problem_id = event["problem"]
            
            elif event_type == "problem_save":
                extra_info = skip_str

            elif event_type == "reset_problem":
                extra_info = skip_str

            elif event_type == "reset_problem_fail":
                extra_info = skip_str

            elif event_type == "save_problem_fail":
                extra_info = skip_str

            elif event_type == "save_problem_success":
                extra_info = skip_str

            elif event_type == "showanswer":
                extra_info = skip_str

            if extra_info != skip_str:
                extra_info += "\n"
                writeToDb(cursor, extra_info)
        #elif data["event_type"] in special_exam_events:
        #    event_type = data["event_type"]
        #    if event_type in ["edx.special_exam.proctored.attempt.created", "edx.special_exam.practice.attempt.created", "edx.special_exam.timed.attempt.created"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.declined"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.deleted", "edx.special_exam.practice.attempt.deleted", "edx.special_exam.timed.attempt.deleted"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.download_software_clicked", "edx.special_exam.practice.attempt.download_software_clicked"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.error", "edx.special_exam.practice.attempt.error"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.ready_to_start", "edx.special_exam.practice.attempt.ready_to_start"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.ready_to_submit", "edx.special_exam.practice.attempt.ready_to_submit", "edx.special_exam.timed.attempt.ready_to_submit"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.rejected"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.review_received"]:
                
        #    elif event_type in ["edx.special_exam.proctored.attempt.started", "edx.special_exam.practice.attempt.started", "edx.special_exam.timed.attempt.started"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.submitted", "edx.special_exam.practice.attempt.submitted", "edx.special_exam.timed.attempt.submitted"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.attempt.verified"]:
        #        extra_info = skip_str
        #    elif event_type in ["edx.special_exam.proctored.option-presented"]:
        #        extra_info = skip_str
        #    if extra_info != skip_str:
                
# except sqlite3.DatabaseError as err:       
#    print("Error: ", err)
#else:
    database.commit();
    return cursor

def handleRequest(cursor, selectStr, fromStr, whereStr = "", orderByStr = "", outFileName = "results.csv"):#handle the request and write results into outFileName, returns outFileName
    #
    scriptStr = "SELECT " + selectStr + " FROM " + fromStr
    #handle where conditions
    if whereStr != "":
        scriptStr += " WHERE " + whereStr
    #handle order conditions
    if orderByStr != "":
        scriptStr += " ORDER BY " + orderByStr
    #scriptStr += '""'
    cursor.execute(scriptStr)
    #adding labels
    outStr = "";
    if selectStr == "*":
         outStr = "user_id,course_name,execute_time,event_type,page,extra_info,event_class"
    else:
        outStr = selectStr
    outStr += '\n'
    #adding raws
    raw = cursor.fetchone()
    while (raw != None):
        strRaw = str(raw)
        strRaw = strRaw[1:-1]
        outStr += strRaw + '\n'
        raw = cursor.fetchone()
    #writing results
    outFile = open(outFileName, "w")
    outFile.write(outStr)
    outFile.close()
    return outFileName

#cursor = openLogs("spbu_ACADRU_spring_2018-TL")
#handleRequest(cursor, "*", "pause_video", "" ,  "user_id", "example.csv")


    