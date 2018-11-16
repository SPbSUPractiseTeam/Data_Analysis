import os.path
import pandas as pd
import numpy as np
from preprocessing.logParser import openLogs

#path to event logs
BASE_DIR = os.path.abspath('test_statistics.ipynb')
BASE_DIR = os.path.dirname(BASE_DIR)
BASE_DIR = BASE_DIR + '/spbu_ACADRU_spring_2018-TL'
cursor = openLogs(BASE_DIR)

#and questions NOT LIKE '__' means that we needn't questions like {}
#and attempts < 4 means that we use only three first attempts, other attempts are not interesting
request = """
        select 
        course_name, problem_id,
        attempts, questions,
        page, grade, max_grade
        from problem_check
        where course_name = "course-v1:spbu+ACADRU+spring_2018"
        and questions NOT LIKE '__'
        and attempts < 4
        """.format("https://courses.openedu.ru/courses/course-v1:spbu+ACADRU+spring_2018/courseware/b434df438c2045eba63afc089d64b3de/244a81ebf8a64b609cd8587bbe18edc5/")
cursor.execute(request)
data = cursor.fetchall()

columns_names = []
for i in cursor.description[:]:
    columns_names.append(i[0])

df = pd.DataFrame(data=data, columns=columns_names)

#changing refer link and cut problem_id
df['page']= df['page'].apply(lambda x: x.split('/handler')[0])
df['problem_id']= df['problem_id'].apply(lambda x: x.split('@')[-1])

#calculating: average grade, median of grade, number of answers for each test
avg=df.groupby(['course_name','problem_id','page','attempts','max_grade'])['grade'].agg([np.mean, np.median, np.size])
avg=avg.reset_index()
avg = avg.rename(columns={'size': 'number_of_solutions'})

#counting percent of right answers on each question
#parsing questions string in two columns: question and result
listForQuestions=pd.DataFrame(columns=('course_name','problem_id','page','question','attempts','result','max_grade'))

for rowCounter in range(df.shape[0]):
    currentAttempt=df.attempts[rowCounter]
    currentPage=df.page[rowCounter]
    currentCourse=df.course_name[rowCounter]
    currentGrade=df.max_grade[rowCounter]
    currentProblem=df.problem_id[rowCounter]
    
    row=(df.questions[rowCounter][1:-1]).split(',')
    for cellRow in row:
        tmprow=cellRow.split(':')
        if tmprow[1]=='True':
            listForQuestions=listForQuestions.append({'course_name':currentCourse,'problem_id':currentProblem,'page':currentPage,'question':tmprow[0],'attempts':currentAttempt,'result':1,'max_grade':currentGrade}, ignore_index=True)
        else:
            listForQuestions=listForQuestions.append({'course_name':currentCourse,'problem_id':currentProblem,'page':currentPage,'question':tmprow[0],'attempts':currentAttempt,'result':0,'max_grade':currentGrade}, ignore_index=True)

listForQuestions['question'] = listForQuestions['question'].map(str.strip) #deleting spaces
listForQuestions['question']=listForQuestions['question'].apply(lambda x: ('"'+x.split('_')[-2] + '_' + x.split('_')[-1]))

#calculating: sum of grades on question and number of answers on question
perc=listForQuestions.groupby(['course_name','problem_id','page', 'attempts','max_grade','question'])['result'].agg([np.sum , np.size])

#calcilating percentage of right answers on each question
perc=100*perc['sum']/perc['size']
perc=perc.reset_index()

#merge questions and percentage of right answers
perc['questions'] = perc['question'].map(str) +':' +perc[0].map(str)
perc=perc.drop(columns=['question', 0])

#merge questions in test
perc=perc.groupby(['course_name','problem_id','page','attempts','max_grade'])['questions'].apply(','.join).reset_index()
perc['questions']='{ ' + perc['questions'] +'}'

#merge results of analysis (average and percentade) into one table
res=pd.merge(avg, perc, on=['course_name','problem_id','page','attempts','max_grade'], how='outer')

#output
course_name=(res['course_name'][0]+ '_test_statistics.json').replace('+', '_').split(':')[1]
#writing json file
my_file = open(course_name, 'w')
my_file.write(res.to_json(orient='records'))
my_file.close()