# Universidade de Aveiro - Physics Department
# 2016/2017 Project - Andre Calatre, 73207
# "Simulation of an epidemic" - 01/7/2017
# Subtracting dataframes

#import numpy as np
import pandas as pd

sqrcon = pd.read_csv('data/sqr_i_maxs.csv', index_col = 0)
spherecon = pd.read_csv('data/sphere_i_maxs.csv', index_col = 0)

dif = sqrcon.subtract(spherecon)

dif.to_csv('data/c_sqr-sphere.csv')
dif.to_excel('data/c_sqr-sphere.xlsx')
