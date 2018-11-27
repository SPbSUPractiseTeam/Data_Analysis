import pandas as pd
import json

def output(res, courseName):
    fileName = courseName + '_tests_statistics.json'
    data_file = open(fileName, 'w')
    if (not res.empty):

        res['subsection']= res['page'].apply(lambda x: x.split('/')[-2]) 
        res['section']= res['page'].apply(lambda x: x.split('/')[-3]) 
        
        res['questions'] = '{"attempt":'+res['attempts'].map(str)+',"mean":'+ res['mean'].map(str)+',"median":'+res['median'].map(str)+',"number_of_solutions":'+res['number_of_solutions'].map(str)+',"max_grade":'+res['max_grade'].map(str)+',"questions":'+res['questions']+'}'
        res=res.drop(columns=['mean', 'attempts','median','number_of_solutions','max_grade'])
        res=res.groupby(['course_name','problem_type','problem_id','page','section','subsection'])['questions'].apply(','.join).reset_index()
        
        res['questions']='{"problem_id":'+res['problem_id'].map(str)+',"attempts":['+ res['questions']+']}'
        res=res.drop(columns=['problem_id'])
        res=res.groupby(['course_name','problem_type','page','section','subsection'])['questions'].apply(','.join).reset_index()
        
        res['questions']='{"subsection":'+res['subsection'].map(str)+',"problem_type":'+res['problem_type']+',"page":'+res['page'].map(str)+ ',"one_type_problems":['+ res['questions']+']}'
        res=res.drop(columns=['page','problem_type','subsection'])
        res=res.groupby(['course_name','section'])['questions'].apply(','.join).reset_index()
        
        res['questions']='{"section":'+res['section'].map(str)+',"subsections":['+res['questions']+']}'
        res=res.drop(columns=['section'])
        res=res.groupby(['course_name'])['questions'].apply(','.join).reset_index()
        
        res['questions']='{"course":'+res['course_name'].map(str)+',"tests":['+res['questions']+']}'
        res=res.drop(columns=['course_name'])
        data_file.write(json.dumps(res['questions'][0]))
    else:
        data_file.write(json.dumps("{}"))
    data_file.close() 
    return fileName
