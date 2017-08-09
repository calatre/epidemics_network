# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 7/6/2017
# Simulation of a (non-spacial) SIR Epidemic Model

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors


#Possible status of a person - Dead, Healthy (but susceptible), Sick
DEAD, HEALTH, SICK = 0, 1, 2

# Colours for visualization: black = dead, green = healthy, red = sick
#Note that apparently for the colormap to work, this list and the bounds list
# must be one larger than the number of different values in the array.
colors_list = ['k', 'g', 'r', 'b', 'b']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)

#Defining the main function:
inf = 1
def iterate_ns(X, cval, rval):
    """Iterate the map according to the epidemic rules."""
    global inf
    turninf = 0
    X1 = np.zeros((ny, nx))
    for ix in range(nx):
        for iy in range(ny):
            rem = np.random.random()
            con = np.random.random()
            #if sick, probability (1-r) of surviving one more turn
            if X[iy,ix] == SICK and rem >= rval:
                X1[iy,ix] = SICK
            #There's a chance cval*inf of contagion, no matter the position
            if X[iy,ix] == HEALTH and con <= cval*inf:
                X1[iy,ix] = SICK
                turninf += 1 #this one adds to the turn's statistics
            if X[iy,ix] == HEALTH and con >= cval*inf:
                X1[iy,ix] = HEALTH
    print('this turn:' + str(turninf))
    inf += turninf
    print ('total inf:' + str(inf))

    return X1


# base probabilities: people born, diseases appear, chance of contagion
cval = 0.0001


#transition probabilities: if sick, subject _s_urvives < dies
rval = 0.01

# map size (number of cells in x and y directions).
nx, ny = 100, 100
# Initialize the map grid.
X  = np.ones((ny, nx))
X[int(nx/2),int(ny/2)] = SICK

#plotting a single frame
fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)#, interpolation='nearest')

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    animate.X = iterate_ns(animate.X, cval, rval)
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X

# Interval between frames (ms).
interval = 2000
anim = animation.FuncAnimation(fig, animate, interval = interval)
plt.show()

