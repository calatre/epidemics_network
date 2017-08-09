# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 15/5/2017
# Multiple Simulations of a SIR Epidemic Model

import numpy as np
import pandas as pd

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

#Possible status of a person - Dead, Healthy (but susceptible), Sick or Immune
DEAD, HEALTH, SICK = 0, 1, 2

#Defining the main function:
def iterate(X, cval, rval):
    """Iterate the map according to the epidemic rules."""

    # The boundary of the map is always empty, so only consider cells
    # indexed from 1 to nx-2, 1 to ny-2
    X1 = np.zeros((ny, nx))
    for ix in range(1,nx-1):
        for iy in range(1,ny-1):
            #if sick, probability (s-i) of surviving one more turn
            if X[iy,ix] == SICK and np.random.random() >= rval:
                X1[iy,ix] = SICK
            #if you're healthy the same, except...
            if X[iy,ix] == HEALTH:
                X1[iy,ix] = HEALTH
                #if a neighbour is sick, there's a chance c of contagion
                for dx,dy in neighbourhood:
                    if X[iy+dy,ix+dx] == SICK and np.random.random() <= cval:
                        X1[iy,ix] = SICK
                        break
    return X1

def count(X):
    """Goes through the map, counting occurences"""
    
    #lets make a row [susceptible, infected, removed]
    susceptible = 0
    infected = 0
    removed = 0
    
    #the iteration rules
    for ix in range(1,nx-1):
        for iy in range(1,ny-1):
            if X[iy,ix] == HEALTH:
                susceptible += 1
            if X[iy,ix] == SICK:
                infected += 1
            if X[iy,ix] == DEAD: 
                removed += 1
            data = np.array([susceptible, infected, removed])
            #print(data)
    return data

# Constructing a Dataframe through iterations
def fill_df(df, X, cval, rval, steps = 200, measure_every = 10):
    '''Pick dataframe-> iterate map-> count variables-> add result as  row'''
    for i in range(steps):
        X1 = iterate(X, cval, rval)
        X = X1
        if i % measure_every == 0:
            data = count(X)
            print(data)
            df = np.vstack((df, data))            
            if data[1] == 0:
                break                   
    return df

# base probabilities: people born, diseases appear, chance of contagion
#c = 0.09

#transition probabilities: if sick, subject is _r_emoved < survives
#r = 0.1

# map size (number of cells in x and y directions).
nx, ny = 100, 100
# Initialize the map grid.
X  = np.ones((ny, nx))
X[int(nx/2),int(ny/2)] = SICK

def multiple_dfs(points,cval, rval):
    '''Make multiple dataframes'''
    print('Starting Data for c = ' + str(cval)+', r = '+ str(rval))
    #Initialize 1st dataframe, fill with first step
    cols = ['Susceptible', 'Infected', 'Removed']
    val = count(X)
    stps, interval = 1000, 10
    matrix = fill_df(val,X, cval, rval, steps = stps, measure_every = interval)
    rows = matrix.shape[0] * interval
    df = pd.DataFrame(matrix , index = range(0,rows,interval), columns = cols)
    #Make multiple dataframes
    for r in range(2, points+1):
        matrix = fill_df(val,X, cval, rval, steps = stps, measure_every = interval)
        rows = matrix.shape[0] * interval
        n = pd.DataFrame(matrix , index = range(0,rows,interval), columns = cols)
        print(n)
        df = pd.concat([df,n], axis = 1).fillna(method='pad')
    #Add average columns at the end    
    df['S_Avg'] = df[df.columns[::3]].mean(axis=1)
    df['I_Avg'] = df[df.columns[1::3]].mean(axis=1)
    df['R_Avg'] = df[df.columns[2::3]].mean(axis=1)
    #df.to_excel('SIR_data_multiple_avg.xlsx', sheet_name = 'c = '+str(cval))
    print('Final Data for c = ' + str(cval)+', r = '+ str(rval))
    print(df)
    return df
    
#Choosing the values for c and r to study
cvalues = [0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]# 
rvalues = [0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]#
#We will have to use an excel writer 
#to capture data in multiple sheets in a xlsx
writer = pd.ExcelWriter('SIR_data_multiple_avg.xlsx')
for cvar in cvalues:
    for rvar in rvalues:
        data = multiple_dfs(10,cvar,rvar)
        data.to_excel(writer,'c='+str(cvar)+'|r='+ str(rvar))
writer.save()
    
