# -*- coding: utf-8 -*-
"""
Created on Thu Oct  22 09:53:54 2020

@author: RP258738, renata.porciunculabaptista@cea.fr

This script simulates bloch equations

"""
import sys, os
import matplotlib.pyplot as plt

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append(os.path.join(sys.path[0],'../Utils/'))
sys.path.append(os.path.join(sys.path[0],'./libs/'))
sys.path.append(os.path.join(sys.path[0],'./parameters/'))

    
# Import homemade
from utils_own.bloch_equations import *
from utils_own.model import getW1fromFAandTau
from utils_own.quantification import *
from parameters.initialization import INITIALIZATION


dt = 0.001
t = np.arange(0,0.3,dt)

Fa_sub = np.array(INITIALIZATION['sub01_y']['FA'])
# Method 1 both together
M0a = [0,0,1]
M0b = [0,0,0.75]
Ma, Mb = getTheoricalValues(0.30, 0.45, [0,0,1], [0,0, 0.75],Fa_sub , INITIALIZATION['calibration'], 'PCr', 'cATP')
plt.plot(Fa_sub,Ma[:], label = 'Mine: PCR Mz')
plt.plot(Fa_sub, Mb[:], label = 'Mine: ATP Mz') # XY equal
plt.legend()
plt.show()

