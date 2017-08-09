# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 24/5/2017
# Plotting Multiple Simulations of a SIR Epidemic Model
# Based on the US unemployment example on Bokeh Website:
#   http://bokeh.pydata.org/en/latest/docs/gallery/unemployment.html


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.mplot3d import Axes3D

#Choosing the values for c and r to study
cvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
rvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]

#Lets open our previously generated maxima csv file
rems = pd.read_csv('data/sqr_r.csv', index_col = 0)
print(rems) #to check it

# reshape to 1D array
rdf = pd.DataFrame(rems.stack()).reset_index()
rdf.apply(pd.to_numeric)


print(rdf) #lets se how it looks like

rdf.round(1) #making sure there's no weird huge numbers

points = rdf.values
x = np.array(points[:,0].astype(float))
y = np.array(points[:,1].astype(float))
z = np.array(points[:,2])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

surf = ax.plot_trisurf(x,y,z, cmap=cm.plasma, linewidth=0.1, alpha = 0.4)
#surf = ax.plot_trisurf(u,v,w, cmap=cm.Reds, linewidth=0.1, alpha = 1)
#fig.colorbar(surf)

ax.xaxis.set_major_locator(MaxNLocator(5))
ax.yaxis.set_major_locator(MaxNLocator(5))
ax.zaxis.set_major_locator(MaxNLocator(10))
ax.set_xlabel('Removal Probability')
ax.set_ylabel('Contagion Probability')
ax.set_zlabel('Removed individuals')

fig.tight_layout()

plt.show()