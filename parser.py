import json
from pprint import pprint

def getCommonInfo(data):
    res = str(data["context"]["user_id"]) +","+ data["context"]["course_id"] + "," + data["time"]
    return res;

inpFileName = "spbu_BIOINF_spring_2018-TL"
outFileName = inpFileName + ".csv"
inpfile = open(inpFileName)
outfile = open(outFileName, "w")
for line in inpfile:
    data = json.loads(line);
    video_events = ["hide_transcript", "edx.video.transcript.hidden","load_video", "edx.video.loaded", "pause_video", "edx.video.paused", "play_video", "edx.video.played", "seek_video", "edx.video.position.changed", "show_transcript", "edx.video.transcript.shown", "speed_change_video", "stop_video", "edx.video.stopped", "video_hide_cc_menu", "video_show_cc_menu"];
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

        if event_type in ["show_transcript", "edx.video.transcript.shown"]:
            event_type = "show_transcript"
            extra_info = str(event["currentTime"])

        if event_type in ["load_video", "edx.video.loaded"]:
            event_type = "load_video"

        if event_type in ["pause_video", "edx.video.paused"]:
            event_type = "pause_video"
            extra_info = str(event["currentTime"])

        if event_type in ["play_video", "edx.video.played"]:
            event_type = "play_video"
            extra_info = str(event["currentTime"])

        if event_type in ["stop_video", "edx.video.stopped"]:
            event_type = "stop_video"
            extra_info = str(event["currentTime"])

        if event_type in ["seek_video", "edx.video.position.changed"]:
            event_type = "seek_video"
            extra_info = str(event["old_time"]) + "," + str(event["new_time"])

        if event_type == "speed_change_video":
            extra_info = str(event["current_time"]) + "," + str(event["old_speed"]) + "," + str(event["new_speed"])

        res = getCommonInfo(data)
        res += "," + event_type + "," + data["page"] + "," + extra_info + '\n';
        outfile.write(res);
outfile.close()
    