import pandas as pd

def output(res, courseName):
    fileName = courseName
    my_file = open(fileName + ".json", 'w')
    my_file.write(res.to_json(orient='records'))
    my_file.close()
    return fileName
