# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 28/6/2017
# Selecting Data from an excel file to another

#import numpy as np
import pandas as pd
from openpyxl import load_workbook

#r = [0, 301, 302, 303, 304, 305, 306]
#desired = ['S_Avg',	'I_Avg',	'R_Avg',	'S_StD',	'I_StD',	'R_StD']
cvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
rvalues = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,
                                                   0.25, 0.5, 0.75, 1]
book = load_workbook('data/ns_shift.xlsx')
writer = pd.ExcelWriter('data/nd_shift.xlsx', engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

for cvar in cvalues:
    for rvar in rvalues:
        print('retrieving...')
        tblnm = 'c='+str(cvar)+'|r='+ str(rvar)
        data = pd.read_excel('data/ns_shift.xlsx', 
                        sheetname = tblnm, index_col = 0)
        print('...retrieved')
        #data.drop(data.columns[r], axis = 1, inplace= True)
        sel = data[:1000]
        print('copying...............................'+str(tblnm))
        sel.to_excel(writer,'c='+str(cvar)+'|r='+ str(rvar))
        print('copied!')
writer.save()
