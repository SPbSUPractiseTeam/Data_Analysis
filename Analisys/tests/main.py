import pandas as pd
import numpy as np

from .content import test_questions_analisys as qa
from .content import tests_analisys as ta
from .output import output as out

def Execute(cursor, courseName):
    #and questions NOT LIKE '__' means that we needn't questions like {}
    #and attempts < 4 means that we use only three first attempts, other attempts are not interesting    
    request = """
        select course_name, page, problem_type, problem_id, attempts, questions, grade, max_grade
        from problem_check
        where questions NOT LIKE '__'
        and attempts < 4
        """
    cursor.execute(request)
    data = cursor.fetchall()

    if (data):
        columns_names = []
        for i in cursor.description[:]:
            columns_names.append(i[0])
            
        df = pd.DataFrame(data=data, columns=columns_names)
        
        #changing refer link and cut problem_id
        df['page']= df['page'].apply(lambda x: x.split('?child')[0])        
        df['problem_id']= df['problem_id'].apply(lambda x: x.split('@')[-1]) 
        
        tmpdf=df.groupby(['course_name','page','problem_type','problem_id','attempts'])['max_grade'].agg([np.max]) 
        tmpdf=tmpdf.rename(columns={'amax': 'max_grade'})        
        
        #calculating: average grade, median of grade, number of answers for each test
        avg = ta.calculateTests(df)
        
        #counting percent of right answers on each question
        #parsing questions string in two columns: question and result
        
        new_cols = df['questions'].str[1:-1]
        new_cols=new_cols.str.split(',').apply(pd.Series, 1).stack()   
        new_cols=new_cols.apply(lambda x: pd.Series(x.split(':')[-1]))         
        new_cols=new_cols.reset_index(level=1)
        new_cols=new_cols.rename(columns={'level_1': 'question', 0:'result'})
        new_cols['question']=new_cols['question'].apply(lambda x: pd.Series(x+1))
        new_cols['result'] = new_cols['result'].map({'True': 1, 'False': 0})
        listForQuestions = pd.DataFrame(df, columns=['course_name','page','problem_type','problem_id','attempts'])
        listForQuestions=listForQuestions.join(new_cols)

        perc = qa.calculateQuestions(listForQuestions)
        
        #merge results of analysis (average and percentade) into one table
        res=pd.merge(avg, perc, on=['course_name','page','problem_type','problem_id','attempts'], how='outer')
        res=pd.merge(res, tmpdf, on=['course_name','page','problem_type','problem_id','attempts'], how='outer')
    else:
        res=""
    return out.output(res, courseName)
