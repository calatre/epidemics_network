# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 14/6/2017
# Multiple Simulations of a SIR Epidemic Model, Spacial Spherical Lattice Model

import numpy as np
import pandas as pd

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

#Possible status of a person - Dead, Healthy (but susceptible), Sick
DEAD, HEALTH, SICK = 0, 1, 2

#Let's define a seed, to ensure reproducibility of results
np.random.seed(73207) #in this case my student number

#Defining the main function, in this case the spherical one:
def iterate_o(X, cval, rval):
    """Iterate the map according to the epidemic rules."""

    #We'll go to boundary. If it goes beyond, check the oposite side then.
    X1 = np.zeros((ny, nx))
    for ix in range(nx):
        for iy in range(ny):
            #if sick, probability (1-rval) of surviving one more turn
            if X[iy,ix] == SICK and np.random.random() >= rval:
                X1[iy,ix] = SICK
            #if you're healthy the same, except...
            if X[iy,ix] == HEALTH:
                X1[iy,ix] = HEALTH
                #...if a neighbour is sick, there's a chance c of contagion
                for dx,dy in neighbourhood:
                    if iy+dy > ny-1: #if neighbour is out of latice,
                        iy = -1      #then neighbour is on the other side
                    if ix+dx > nx-1:
                        ix = -1
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
    for ix in range(nx):
        for iy in range(ny):
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
        X1 = iterate_o(X, cval, rval)
        X = X1
        if i % measure_every == 0:
            data = count(X)
            print(data)
            df = np.vstack((df, data))            
            if data[1] == 0:
                break                   
    return df

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
    #Add also standard deviation columns at the end    
    df['S_StD'] = df[df.columns[::3]].std(axis=1)
    df['I_StD'] = df[df.columns[1::3]].std(axis=1)
    df['R_StD'] = df[df.columns[2::3]].std(axis=1)
    #df.to_excel('SIR_data_multiple_avg.xlsx', sheet_name = 'c = '+str(cval))
    print('Final Data for c = ' + str(cval)+', r = '+ str(rval))
    print(df)
    return df
    
#Choosing the values for c and r to study
cvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]# 
rvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]#
           
#We will have to use an excel writer 
#to capture data in multiple sheets in a xlsx
writer = pd.ExcelWriter('SIR_sphere_data_multiple_avg.xlsx')
for cvar in cvalues:
    for rvar in rvalues:
        data = multiple_dfs(100,cvar,rvar)
        data.to_excel(writer,'c='+str(cvar)+'|r='+ str(rvar))
writer.save()
    
