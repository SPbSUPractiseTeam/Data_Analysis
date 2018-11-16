import pandas as pd
import numpy as np

def calculateQuestions(listForQuestions)

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

    return perc

