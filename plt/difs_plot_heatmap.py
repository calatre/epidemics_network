# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 03:39:55 2017

@author: mrp
"""
import pandas as pd
import seaborn as sns


df = pd.read_csv('data/c_sqr-sphere.csv', index_col=0)

# _r reverses the normal order of the color map 'RdYlGn'
sns.heatmap(df, cmap='RdYlGn_r', linewidths=0.5, 
            annot=True, annot_kws={"size": 10}, fmt='g')