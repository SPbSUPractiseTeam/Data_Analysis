import pandas as pd
import numpy as np

def calculateTests(df):
    avg=df.groupby(['course_name','problem_id','page','attempts','max_grade'])['grade'].agg([np.mean, np.median, np.size])
    avg=avg.reset_index()
    avg = avg.rename(columns={'size': 'number_of_solutions'})
    return avg
