# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 7/4/2017
# Simulation of SIR Epidemic Model

import numpy as np
import pandas as pd

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

#Possible status of a person - Dead, Healthy (but susceptible), Sick or Immune
DEAD, HEALTH, SICK = 0, 1, 2

#Defining the main function:
def iterate(X):
    """Iterate the map according to the epidemic rules."""

    # The boundary of the map is always empty, so only consider cells
    # indexed from 1 to nx-2, 1 to ny-2
    X1 = np.zeros((ny, nx))
    for ix in range(1,nx-1):
        for iy in range(1,ny-1):
            #if sick, probability (s-i) of surviving one more turn
            if X[iy,ix] == SICK and np.random.random() <= s:
                X1[iy,ix] = SICK
            #if you're healthy the same, except...
            if X[iy,ix] == HEALTH:
                X1[iy,ix] = HEALTH
                #if a neighbour is sick, there's a chance c of contagion
                for dx,dy in neighbourhood:
                    if X[iy+dy,ix+dx] == SICK and np.random.random() <= c:
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
            if X[iy,ix] == DEAD: 
                removed += 1
            if X[iy,ix] == SICK:
                infected += 1
            if X[iy,ix] == HEALTH:
                susceptible += 1
            data = np.array([susceptible, infected, removed])
    return data

# Constructing a Dataframe through iterations
def fill_df(df, X, steps = 200, measure_every = 10):
    '''Pick dataframe-> iterate map-> count variables-> add result as  row'''
    for i in range(steps):
        X1 = iterate(X)
        X = X1
        if i % measure_every == 0: 
            data = count(X)
            df = np.vstack((df, data))
            if data[1] == 0:
                break
    return df

# base probabilities: people born, diseases appear, chance of contagion
c = 0.09

#transition probabilities: if sick, subject _s_urvives < dies
s = 0.9

# map size (number of cells in x and y directions).
nx, ny = 100, 100
# Initialize the map grid.
X  = np.ones((ny, nx))
X[int(nx/2),int(ny/2)] = SICK

#Initialize dataframe, fill with first step
cols = ['Susceptible', 'Infected', 'Removed']
val = count(X)
stps, interval = 200, 10
matrix = fill_df(val,X, steps = stps, measure_every = interval)
rows = matrix.shape[0] * interval
df = pd.DataFrame(matrix , index = range(0,rows,interval), columns = cols)

df.to_excel('SIR_data_1.xlsx', sheet_name = '1st_data')
