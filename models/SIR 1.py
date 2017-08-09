# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 7/4/2017
# Simulation of SIR Epidemic Model

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

#Possible status of a person - Dead, Healthy (but susceptible), Sick
DEAD, HEALTH, SICK = 0, 1, 2

#Defining the main function:
def iterate_sq(X, cval, rval):
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


# base probabilities: people born, diseases appear, chance of contagion
cval = 0.07


#transition probabilities: if sick, subject _s_urvives < dies
rval = 0.2 

# map size (number of cells in x and y directions).
nx, ny = 102, 102
# Initialize the map grid.
X  = np.ones((ny, nx))
X[int(nx/2),int(ny/2)] = SICK

# Colours for visualization: black = dead, green = healthy, red = sick
#Note that apparently for the colormap to work, this list and the bounds list
# must be one larger than the number of different values in the array.
colors_list = ['k', 'g', 'r', 'b', 'b']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)

#plotting a single frame
fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)#, interpolation='nearest')

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    animate.X = iterate_sq(animate.X, cval, rval)
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X

# Interval between frames (ms).
interval = 1
anim = animation.FuncAnimation(fig, animate, interval=interval)
plt.show()

