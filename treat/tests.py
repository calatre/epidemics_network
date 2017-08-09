# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 18:40:11 2017

@author: mrp
"""

import matplotlib.pyplot as plt
import numpy as np

types = ('sci', 'web', 'eng')
n = np.array(len(types))
vals = [5,7,3]

plt.bar(n,vals)
plt.xticks(n, types)

plt.show()
