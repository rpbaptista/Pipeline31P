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
from parameters.initialization import INITIALIZATION


dt = 0.001
t = np.arange(0,0.1,dt)
N = np.max(t.shape)
TE = INITIALIZATION['calibration']['TE']
TR = INITIALIZATION['calibration']['TR']
FA = INITIALIZATION['calibration']['FA']
t_A = INITIALIZATION['calibration']['PCr']
t_B = INITIALIZATION['calibration']['cATP']
w1 = 0
kab = 0 #0.3
kba = 0 #1.5

# Method 1 both together
M0a = [1,0,0]
M0b = [0.75,0,0]
M = np.zeros((6, N))
for i in range(N):
    M[:,i] = magnetization_signal(t[i], 0, 300, M0a, M0b, kab, kba,t_A, t_B, w1)
 

# method 2 - separately - Works
# Apcr, bpcr = freeprecess(T=dt,
#                         T1=INITIALIZATION['calibration']['PCr']['T1'],
#                         T2=INITIALIZATION['calibration']['PCr']['T2e'],
#                         df=0)

# Mpcr = np.zeros((3, N))
# Mpcr[:,0]= [1,0,0]
# for i in range(N-1):
#     Mpcr[:,i+1] = np.dot(Apcr,Mpcr[:,i])+bpcr

# plt.plot(t,Mpcr[0,:], label ='Freeprecess: PCr Mx')
# plt.plot(t,Mpcr[1,:], label = 'Freeprecess: PCr My')
# plt.plot(t,Mpcr[2,:], label = 'Freeprecess: PCr Mz')
# plt.plot(t,M[0,:], label ='Mine: PCr Mx, delta{0:.3f}'.format(np.sum(Mpcr[0,:]-M[0,:]))) # XY equal
# plt.plot(t,M[1,:], label = 'Mine: PCr My, delta{0:.3f}'.format(np.sum(Mpcr[1,:]-M[1,:])))
# plt.plot(t,M[2,:], label = 'Mine: PCR Mz, delta{0:.3f}'.format(np.sum(Mpcr[2,:]-M[2,:])))
# plt.legend()
# plt.show()



Aatp, batp = freeprecess(T=dt,
                        T1=INITIALIZATION['calibration']['cATP']['T1'],
                        T2=INITIALIZATION['calibration']['cATP']['T2e'],
                        df=300)
Matp = np.zeros((3, N))
Matp[:,0]= [0.75,0,0]

for i in range(N-1):
    Matp[:,i+1] = np.dot(Aatp,Matp[:,i])+batp

plt.plot(t,Matp[0,:], label ='Freeprecess: ATP Mx')
plt.plot(t,Matp[1,:], label = 'Freeprecess: ATP My')
plt.plot(t,Matp[2,:], label = 'Freeprecess: ATP Mz')
plt.plot(t,M[3,:], label ='Mine: ATP Mx, delta{0:.3f}'.format(np.sum(Matp[0,:]-M[0,:]))) # XY equal
plt.plot(t,M[4,:], label = 'Mine: ATP My, delta{0:.3f}'.format(np.sum(Matp[1,:]-M[1,:]))) # XY equal
plt.plot(t,M[5,:], label = 'Mine: ATP Mz, delta{0:.3f}'.format(np.sum(Matp[2,:]-M[2,:]))) # XY equal
plt.legend()
plt.show()
