import pandas as pd
import numpy as np

def calculateQuestions(listForQuestions):

    #calculating: sum of grades on question and number of answers on question
    perc=listForQuestions.groupby(['course_name','page','problem_type','problem_id','attempts','question'])['result'].agg([np.sum , np.size])

    #calcilating percentage of right answers on each question
    perc=100*perc['sum']/perc['size']
    perc=perc.reset_index()

    #merge questions and percentage of right answers
    perc['questions'] = '{"question":'+perc['question'].map(str) +',"percent_of_right_answers":' +perc[0].map(str)+'}'
    perc=perc.drop(columns=['question', 0])

    #merge questions in test
    perc=perc.groupby(['course_name','page','problem_type','problem_id','attempts'])['questions'].apply(','.join).reset_index()
    perc['questions']='[' + perc['questions'] +']'

    return perc

