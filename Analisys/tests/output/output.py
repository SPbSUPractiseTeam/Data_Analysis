import pandas as pd
import json

def output(res, courseName):
    fileName = courseName + '_tests_statistics.json'
    data_file = open(fileName, 'w')
    if (res):
        res['questions'] = '{"attempt":'+res['attempts'].map(str)+',"mean":'+ res['mean'].map(str)+',"median":'+res['median'].map(str)+',"number_of_solutions":'+res['number_of_solutions'].map(str)+',"max_grade":'+res['max_grade'].map(str)+',"questions":'+res['questions']+'}'
        res=res.drop(columns=['mean', 'attempts','median','number_of_solutions','max_grade'])
        res=res.groupby(['course_name','problem_id','page'])['questions'].apply(','.join).reset_index()
        res['questions']='{"problem_id":'+res['problem_id'].map(str)+',"page":'+res['page'].map(str)+',"attempts":['+ res['questions']+']}'
        res=res.drop(columns=['problem_id', 'page'])
        res=res.groupby(['course_name'])['questions'].apply(','.join).reset_index()
        res['questions']='{"course":'+res['course_name'].map(str)+',"tests":['+res['questions']+']}'
        res=res.drop(columns=['course_name'])
        data_file.write(json.dumps(res['questions'][0]))
    else:
        data_file.write(json.dumps("{}"))
    data_file.close() 
    return fileName
