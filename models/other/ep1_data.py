#Universidade de Aveiro - Physics Department
#2016/2017 Project - Andre Calatre, 73207
#"Simulation of an epidemic" - 14/3/2017
#The following code has been based on:
#Forest Fire Model from http://scipython.com/blog/the-forest-fire-model/ 


import numpy as np
import pandas as pd

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

#Possible status of a person - Dead, Healthy (but susceptible), Sick or Immune
DEAD, HEALTH, SICK, IMM = 0, 1, 2, 3

#Defining the main function:
def iterate(X):
    """Iterate the map according to the epidemic rules."""

    # The boundary of the map is always empty, so only consider cells
    # indexed from 1 to nx-2, 1 to ny-2
    X1 = np.zeros((ny, nx))
    for ix in range(1,nx-1):
        for iy in range(1,ny-1):
            #if empty, probability p of spawning new people
            if X[iy,ix] == DEAD and np.random.random() <= p:
                X1[iy,ix] = HEALTH
            #if sick, probability i of cure and becoming immune
            if X[iy,ix] == SICK and np.random.random() <= i:
                X1[iy,ix] = IMM 
            #if sick, probability (s-i) of surviving one more turn
            if X[iy,ix] == SICK and np.random.random() <= s:
                X1[iy,ix] = SICK
            #if you're immune, you're not going anywhere
            if X[iy,ix] == IMM:
                X1[iy,ix] = IMM
            #if you're healthy the same, except...
            if X[iy,ix] == HEALTH:
                X1[iy,ix] = HEALTH
                #if a neighbour is sick, there's a chance c of contagion
                for dx,dy in neighbourhood:
                    if X[iy+dy,ix+dx] == SICK and np.random.random() <= c:
                        X1[iy,ix] = SICK
                        break
                #and once in a while, diseases appear out of nowhere
                else:
                    if np.random.random() <= d:
                        X1[iy,ix] = SICK
    return X1

def count(X):
    """Goes through the map, counting occurences"""
    
    #lets make a row [healthy, infected, immune, dead]
    healthy = 0
    infected = 0
    immune = 0
    dead = 0
    
    #the iteration rules
    for ix in range(1,nx-1):
        for iy in range(1,ny-1):
            if X[iy,ix] == DEAD: 
                dead += 1
            if X[iy,ix] == SICK:
                infected += 1
            if X[iy,ix] == IMM:
                immune += 1
            if X[iy,ix] == HEALTH:
                healthy += 1
            data = np.array([healthy, infected, immune, dead])
    return data

# Constructing a Dataframe through iterations
def fill_df(df, X, steps = 1000, measure_every = 10):
    '''Pick dataframe-> iterate map-> count variables-> add result as  row'''
    for i in range(steps):
        X1 = iterate(X)
        X = X1
        if i % measure_every == 0: 
            data = count(X)
            df = np.vstack((df, data))
    return df
    
    
# The initial fraction of the map occupied by people.
ppl_fraction = 1

# base probabilities: people born, diseases appear, chance of contagion
p, d, c = 0.1, 0.001, 0.5

#transition probabilities: if sick, subject gets _i_mmune < _s_urvives < dies
i, s = 0.1, 0.9
# map size (number of cells in x and y directions).
nx, ny = 100, 100
# Initialize the map grid.
X  = np.zeros((ny, nx))
X[1:ny-1, 1:nx-1] = np.random.randint(0, 2, size=(ny-2, nx-2))
X[1:ny-1, 1:nx-1] = np.random.random(size=(ny-2, nx-2)) < ppl_fraction


#Initialize dataframe, fill with first step
cols = ['healthy', 'infected', 'immune', 'dead']
val = count(X)
stps, interval = 500, 10
matrix = fill_df(val,X, steps = stps, measure_every = interval)
df = pd.DataFrame(matrix , index = range(0,stps+1,interval), columns = cols)

df.to_excel('epidemics_data_fast.xlsx', sheet_name = '1s_data')





