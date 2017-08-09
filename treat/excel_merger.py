# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 28/6/2017
#Merging multiple exel files in one

#import numpy as np
import pandas as pd
from openpyxl import load_workbook

r = [0, 301, 302, 303, 304, 305, 306]
#desired = ['S_Avg',	'I_Avg',	'R_Avg',	'S_StD',	'I_StD',	'R_StD']
cvalues = [#0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
rvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
book = load_workbook('SIR_sphere_data_light.xlsx')
writer = pd.ExcelWriter('SIR_sphere_data_light.xlsx', engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

for cvar in cvalues:
    for rvar in rvalues:
        tblnm = 'c='+str(cvar)+'|r='+ str(rvar)
        data = pd.read_excel('sdat/SIR_sphere_data_multiple_avg25-100.xlsx', 
                        sheetname = tblnm, parse_cols = r, index_col = 0)
        #data.drop(data.columns[r], axis = 1, inplace= True)
        print('copying...............................'+str(tblnm))
        data.to_excel(writer,'c='+str(cvar)+'|r='+ str(rvar))
writer.save()
