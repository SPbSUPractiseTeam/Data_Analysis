import pandas as pd

def output(res, courseName):
    fileName = courseName + '_tests_statistics.json'
    my_file = open(fileName, 'w')
    my_file.write(res.to_json(orient='records'))
    my_file.close()
    return fileName
