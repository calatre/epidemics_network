# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 16/5/2017
# Plotting Multiple Simulations of a SIR Epidemic Model

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

#Choosing the values for c and r to study
cvalues = [0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]#  
rvalues = [0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1]#

maxs = pd.read_csv('infection maxima.csv', index_col = 0)

x = maxs.columns
y = maxs.index
X,Y = np.meshgrid(x,y)
Z = maxs
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z)

#fig = plt.figure()
#ax = fig.gca(projection='3d')

#surf = ax.plot_surface(X, Y, maxs)
#surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
#    linewidth=0, antialiased=False)
#ax.set_zlim(-1.01, 1.01)

#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

#fig.colorbar(surf, shrink=0.5, aspect=5)
#plt.title('Original Code')

plt.show()

print(maxs)




