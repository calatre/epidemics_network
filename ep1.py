#Universidade de Aveiro - Physics Department
#2016/2017 Project - Andre Calatre, 73207
#"Simulation of an epidemic" - 1/3/2017
#The following code has been based on:
#Forest Fire Model from http://scipython.com/blog/the-forest-fire-model/ 


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import colors

# Displacements from a cell to its eight nearest neighbours
neighbourhood = ((-1,-1), (-1,0), (-1,1), (0,-1), (0, 1), (1,-1), (1,0), (1,1))

#Possible status of a person - Dead, Healthy (but susceptible), Sick or Immune
DEAD, HEALTH, SICK, IMM = 0, 1, 2, 3

# Colours for visualization: black = dead, green = healthy, red = sick
# and blue = immune. 
#Note that apparently for the colormap to work, this list and the bounds list
# must be one larger than the number of different values in the array.
colors_list = ['k', 'g', 'r', 'b', 'b']
cmap = colors.ListedColormap(colors_list)
bounds = [0,1,2,3,4]
norm = colors.BoundaryNorm(bounds, cmap.N)

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
            #if not dead, they can die from natural causes
            if X[iy,ix] != DEAD and np.random.random() <= (1/e):
                X1[iy,ix] = DEAD
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

# The initial fraction of the map occupied by people.
ppl_fraction = 1

# base probabilities: people born, diseases appear, chance of contagion
p, d, c = 0.1, 0.001, 0.5

#transition probabilities: if sick, subject gets _i_mmune < _s_urvives < dies
i, s = 0.1, 0.9

#age expectancy: people can die of old age
e = 60

# map size (number of cells in x and y directions).
nx, ny = 100, 100
# Initialize the map grid.
X  = np.zeros((ny, nx))
X[1:ny-1, 1:nx-1] = np.random.randint(0, 2, size=(ny-2, nx-2))
X[1:ny-1, 1:nx-1] = np.random.random(size=(ny-2, nx-2)) < ppl_fraction

#plotting a single frame
fig = plt.figure(figsize=(25/3, 6.25))
ax = fig.add_subplot(111)
ax.set_axis_off()
im = ax.imshow(X, cmap=cmap, norm=norm)#, interpolation='nearest')

# The animation function: called to produce a frame for each generation.
def animate(i):
    im.set_data(animate.X)
    animate.X = iterate(animate.X)
# Bind our grid to the identifier X in the animate function's namespace.
animate.X = X

# Interval between frames (ms).
interval = 1
anim = animation.FuncAnimation(fig, animate, interval=interval)
plt.show()