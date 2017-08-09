# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 24/6/2017
# Multiple Simulations of a SIR Epidemic Model, non_Spacial Model

import numpy as np
import pandas as pd

#Let's define a seed, to ensure reproducibility of results
np.random.seed(73207) #in this case my student number

cols = ['Susceptible', 'Infected', 'Removed']

p = 8 / 10000
#Defining the main function, in this case a numerical one based on distributions:
def iterate_ns_numerical(cval, rval, n_individuals = 10000, n_trials = 100,
                         n_iter = 2000):
    """Iterate a binomial distribution according to the epidemic rules."""
    print('Starting Data for c = ' + str(cval)+', r = '+ str(rval))
    S = n_individuals - 1
    I = 1
    R = 0
    i = 0
    line = np.array([S,I,R])
    matrix = line
    for n in range(n_iter):
        i += 1
        c = ( 1 - (1 - cval*p) ** I)
        print('c prob: ' + str(c))
        nI = 0
        if S > 0:
            nI = np.random.binomial(S, c, n_trials).mean()
        print('new inf: ' + str(nI))
        nR = np.random.binomial(I, p*rval, n_trials).mean()
        print('new rem: ' + str(nR))
        R += nR
        I = (I + nI - nR)
        if I < 0:
            R += 0 - I
            I = 0
        S = n_individuals - I - R
        if S <= 0:
            S = 0
        line = np.array([S,I,R])
        print(line)
        if i % 10 == 0:
            matrix = np.vstack((matrix, line))  
            print('Constant Population:' + str(line.sum()==n_individuals))
    print('Final Data for c = ' + str(cval)+', r = '+ str(rval))
    df = pd.DataFrame(matrix, columns = cols).round(2)
    print(df)
    return df

#Choosing the values for c and r to study
cvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]# 
rvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]#
#We will have to use an excel writer 
#to capture data in multiple sheets in a xlsx
writer = pd.ExcelWriter('data/SIR_ns_data_shift.xlsx')
i=0
save_every = 10
for cvar in cvalues:
    for rvar in rvalues:
        data = iterate_ns_numerical(cvar, rvar, 10000, 100)
        data.to_excel(writer,'c='+str(cvar)+'|r='+ str(rvar))
writer.save()

