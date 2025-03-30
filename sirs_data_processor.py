import pandas as pd
from math import sqrt
import numpy as np
import scipy.stats as st

#load sirs data 
#sirs_math=pd.read_csv('sirs_data_math.csv')
#sirs_engineering=pd.read_csv('sirs_data_engineering.csv')

#get row(s) to analyze
#molnar=sirs_math.loc[5200]
#antoine=sirs_engineering.loc[1193]


def pRow(row):
    #indices for each questions data
    iterators=[list(range(7,12)),list(range(13,18)),list(range(19,24)),list(range(25,30)),list(range(31,36)),
            list(range(37,42)),list(range(43,48)),list(range(49,54)),list(range(55,60)),list(range(61,66))]

    #loop through questions and calculate means/errors
    scores=[]
    errors=[]
    for set in iterators:
        q1=row[set[0]]
        q2=row[set[1]]
        q3=row[set[2]]
        q4=row[set[3]]
        q5=row[set[4]]

    
        n=(q1+q2+q3+q4+q5)
        mean=((q1*1)+(q2*2)+(q3*3)+(q4*4)+(q5*5))/n
        std_dev=((((mean-1)**2)*q1)+(((mean-2)**2)*q2)+(((mean-3)**2)*q3)+(((mean-4)**2)*q4)+(((mean-5)**2)*q5))/(n-1)
        std_err=std_dev/sqrt(n)

        scores.append(mean)
        errors.append(std_err)
        
    #switch the sign of question 8s error 

    errors[7]=-errors[7]

    #calculate final score/error and subtract one standard error from final score
    scores_adj=np.array(scores)-np.array(errors)

    return scores_adj

#out=pRow(antoine)
