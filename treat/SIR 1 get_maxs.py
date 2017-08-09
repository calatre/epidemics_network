# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 16/5/2017
# Plotting Multiple Simulations of a SIR Epidemic Model

#import numpy as np
import pandas as pd

#Choosing the values for c and r to study
cvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
rvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
i = 0
maxs = pd.DataFrame(index=rvalues, columns = cvalues)

for cvar in cvalues:
    for rvar in rvalues:
        i += 1
        tblnm = 'c='+str(cvar)+'|r='+ str(rvar)
        data = pd.read_excel('data/sphere_light.xlsx', sheetname = tblnm)
        print('retrieving max for... '+str(tblnm))
        point = data['I_Avg'].max()
        print(point)
        maxs.set_value(rvar,cvar,point)
        print(maxs)
print('The Final Table is...')    
print(maxs)
print('Saving...')
maxs.to_csv('data/sphere_i_maxs.csv')
print('Saved!')
maxs.plot()





