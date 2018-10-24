import json
import sqlite3
from pprint import pprint

def openLogs(inpFileName):#convert logs into database returns cursor, needed for requests
    skip_str = "skip_this"
    def getCommonInfo(data):
        res = str(data["context"]["user_id"]) +",'"+ data["context"]["course_id"] + "','" + data["time"]+"'"
        return res;

    #inpFileName = "spbu_BIOINF_spring_2018-TL"
    databaseName = inpFileName + ".sqlite"
    inpfile = open(inpFileName)
    #try:
    database = sqlite3.connect(databaseName)
    cursor = database.cursor()
    cursor.executescript("""
        DROP TABLE IF EXISTS events;
        CREATE TABLE events
        (
            user_id INT
            ,course_name varchar(300)
            ,execute_time varchar(100)
            ,event_type varchar(100)
            ,page varchar(300)
            ,extra_info varchar(500)
            ,event_class varchar(20)
        )
    """)
    for line in inpfile:
        data = json.loads(line);
        video_events = ["hide_transcript", "edx.video.transcript.hidden","load_video", "edx.video.loaded", "pause_video", "edx.video.paused", "play_video", "edx.video.played", "seek_video", "edx.video.position.changed", "show_transcript", "edx.video.transcript.shown", "speed_change_video", "stop_video", "edx.video.stopped", "video_hide_cc_menu", "video_show_cc_menu"];
        problem_events = ["edx.problem.hint.demandhint_displayed", "edx.problem.hint.feedback_displayed", "problem_check", "problem_check_fail", "problem_graded", "problem_rescore", "problem_rescore_fail", "problem_reset", "problem_save", "problem_show", "reset_problem", "reset_problem_fail", "save_problem_fail", "save_problem_success", "showanswer"];
        if (data["event_type"] in video_events + ["mobile"]):
            if data["event_type"] == "mobile":
                event_type = data["name"]
            else: 
                event_type = data["event_type"]

            extra_info = ""
            event = json.loads(data["event"])
            if event_type in ["hide_transcript", "edx.video.transcript.hidden"]:
                event_type = "hide_transcript"
                extra_info = str(event["currentTime"])

            elif event_type in ["show_transcript", "edx.video.transcript.shown"]:
                event_type = "show_transcript"
                extra_info = str(event["currentTime"])

            elif event_type in ["load_video", "edx.video.loaded"]:
                event_type = "load_video"

            elif event_type in ["pause_video", "edx.video.paused"]:
                event_type = "pause_video"
                extra_info = str(event["currentTime"])

            elif event_type in ["play_video", "edx.video.played"]:
                event_type = "play_video"
                extra_info = str(event["currentTime"])

            elif event_type in ["stop_video", "edx.video.stopped"]:
                event_type = "stop_video"
                extra_info = str(event["currentTime"])

            elif event_type in ["seek_video", "edx.video.position.changed"]:
                event_type = "seek_video"
                extra_info = str(event["old_time"]) + "," + str(event["new_time"])

            elif event_type == "speed_change_video":
                extra_info = str(event["current_time"]) + "," + str(event["old_speed"]) + "," + str(event["new_speed"])

            else:
                extra_info = skip_str

            if extra_info != skip_str:
                res = getCommonInfo(data)
                res += ",'" + event_type + "','" + data["page"] + "','" + extra_info + "','video'\n";
                write_to_database = "insert into events values (" + res + ");"
                cursor.execute(write_to_database)
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
                    for key in event["submission"]:
                        extra_info += key + ":" + str(event["submission"][key]["correct"]) + " "
                    extra_info += ", " + str(event["grade"]) + ", " + str(event["max_grade"])
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
                res = getCommonInfo(data)
                res += ",'" + event_type + "','" + problem_id + "','" + extra_info + "','Xblock'\n";
                write_to_database = "insert into events values (" + res + ");"
                cursor.execute(write_to_database)
# except sqlite3.DatabaseError as err:       
#    print("Error: ", err)
#else:
    database.commit();
    return cursor

def handleRequest(cursor, selectStr = "*", whereStr = "", orderByStr = "", outFileName = "results.csv"):#handle the request and write results into outFileName, returns outFileName
    #
    scriptStr = "SELECT " + selectStr + " FROM events"
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

cursor = openLogs("spbu_ACADRU_spring_2018-TL")
handleRequest(cursor, "*", "event_class = 'Xblock'", "user_id", "example.csv")


    
