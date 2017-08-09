# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 16/5/2017
# Plotting Multiple Simulations of a SIR Epidemic Model

#import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams['lines.linewidth'] = 0.2
rcParams['axes.linewidth'] = 0.1 #set the value globally
#Choosing the values for c and r to study
cvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
rvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
#xlab = range(0,501,10)
i = 0

#box = {'facecolor':'yellow', 'alpha':0.9, 'pad':2}
#plt.figure(figsize = (20,30))
for cvar in cvalues:
    for rvar in rvalues:
        i += 1
        print('Working...')
        tblnm = 'c='+str(cvar)+'|r='+ str(rvar)
        data = pd.read_excel('data/SIR_ns_data_shift.xlsx', sheetname = tblnm)
        print('plotting...............................'+str(tblnm))
        #print(data['S_Avg'])
        plt.subplot(14,14,i)
        y1 = data['Susceptible']
        y2 = data['Infected'] 
        y3 = data['Removed'] 
        #e1 = data['nS_StD']
        #e2 = data['nI_StD']
        #e3 = data['nR_StD']
        #ind = y1.index.values
        plt.plot(y1,'g-')
        #plt.fill_between(ind, y1-e1, y1+e1, linewidth=0,
                         #facecolor = 'g', alpha = 0.3, antialiased = True)
        plt.plot(y2,'r-')
        #plt.fill_between(ind, y2-e2, y2+e2, linewidth=0,
                         #facecolor = 'r', alpha = 0.3, antialiased = True)
        plt.plot(y3,'b-')
       # plt.fill_between(ind, y3-e3, y3+e3, linewidth=0,
                         #facecolor = 'b', alpha = 0.2, antialiased = True)
        plt.axis([0,250,0,10000])
        #plt.text(300,9500,tblnm, bbox= box)
        plt.title('c*p='+str(cvar)+'|r='+ str(rvar), size=4, y=0.75)#, loc='right')
        plt.subplots_adjust(bottom=0.01, right=0.99, top=0.97, left=0.01,
                                                       hspace=.4, wspace=.08)
        #plt.xticks([])
        #plt.yticks([])
        plt.tick_params(labelbottom='off', labelleft='off', width = 0.05)  
        plt.grid(True, linewidth = 0.05)
        #plt.tight_layout()
        
#plt.show()
plt.savefig('img/test.png', format='png', dpi=1200, figsize=(40,30))



