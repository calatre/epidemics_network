# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 17:43:17 2017

@author: mrp
"""

#import numpy as np
import pandas as pd
from openpyxl import load_workbook

#r = [292, 293, 294, 295, 296, 297]
#desired = ['S_Avg',	'I_Avg',	'R_Avg',	'S_StD',	'I_StD',	'R_StD']
cvalues = [ 0.07]
rvalues = [ 0.02]
book = load_workbook('data/Raw Spherical Data/SIR_sphere_data_multiple_avg007-8_alternative_testing.xlsx')
writer = pd.ExcelWriter('data/Raw Spherical Data/SIR_sphere_data_multiple_avg007-8_alternative_testing.xlsx', engine='openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

for cvar in cvalues:
    for rvar in rvalues:
        tblnm = 'alt|c='+str(cvar)+'|r='+ str(rvar)
        df = pd.read_excel('data/Raw Spherical Data/SIR_sphere_data_multiple_avg007-8_alternative_testing.xlsx', 
                        sheetname = tblnm)
        #df.drop(df.columns[r], axis = 1, inplace= True)
        print('copying...............................'+str(tblnm))
        #Add average columns at the end    
        df['nS_Avg'] = df[df.columns[::3]].mean(axis=1)
        df['nI_Avg'] = df[df.columns[1::3]].mean(axis=1)
        df['nR_Avg'] = df[df.columns[2::3]].mean(axis=1)
        #Add also standard deviation columns at the end    
        df['nS_StD'] = df[df.columns[::3]].std(axis=1)
        df['nI_StD'] = df[df.columns[1::3]].std(axis=1)
        df['nR_StD'] = df[df.columns[2::3]].std(axis=1)
        df.to_excel(writer,'alt|c='+str(cvar)+'2|r='+ str(rvar))
writer.save()

