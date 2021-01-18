# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""
# Systems libraries
import sys, os

sys.path.append(os.path.join(sys.path[0],'../Utils/'))

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import nibabel as nib 
from scipy import stats

# My libraries
from utils_own.b1_mapping import *
from utils import openArrayImages

init = INITIALIZATION['b1_database'] 


# Simulating data
S0 = 1
N_iterations = 1000


# True values
# Noise

alpha_0 = np.linspace(5, 30, num=15) # np.array([25,35,45] )
results_monte_carlo = np.zeros((alpha_0.size,N_iterations))
for j in range(alpha_0.size):
    S_alpha = equation_B1(init['T1'] ,init['TR'],get_sequence_alpha(alpha_0[j] ) , S0)
    print(S_alpha)
    std = 0.1*S_alpha[0]  
    mean = 1*S_alpha[0]  
    noise =  std * np.random.randn(S_alpha.size,N_iterations) + mean

    for i in range(N_iterations):
        y_obs = S_alpha +noise[:,i]
        pop, _ = curve_fit(function_B1_double,
                                [init['T1'] ,init['TR']],
                                y_obs,
                                maxfev=600)
                                
        results_monte_carlo[j,i], a = pop #
#plt.plot(get_sequence_alpha(results_monte_carlo).T)   
plt.plot(alpha_0, alpha_0, '-', label='Ground truth' )#
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1), '-', label='Mean' )#
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1)+np.std(results_monte_carlo,axis=1), label='m + std')
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1)-np.std(results_monte_carlo,axis=1), label='m - std')
plt.legend()
#plt.plot(get_sequence_alpha(alpha_0), results_monte_carlo)
plt.show()



"""
# REAL DATA
keys_sub = search_keys_sub(init)
for sub in keys_sub:
    SFdata = openArrayImages(init[sub])
    shape = SFdata.shape
    # FITT
    y_values_alpha_1 = SFdata[0,:,:,:].reshape((-1,1))
    y_values_alpha_2 = SFdata[1,:,:,:].reshape((-1,1))

    y_values = np.hstack((y_values_alpha_1 ,y_values_alpha_2))
   
    results = np.zeros(y_values[:,0].shape)
    for i in range(len(y_values[:,0])):
        pop, _ = curve_fit(function_B1,
                                [init['T1'] ,init['TR']],
                                y_values[i,:]  )
        a , results[i] = pop                        
    array = results.reshape((shape[1], shape[2], shape[3]))
    #  
    print("Mean",results.mean())
    img = nib.Nifti1Image(np.squeeze(array), np.eye(4))
    nib.save(img, "result_carte_b1_"+sub+".nii")

# alpha = np.arange(90)
# keys_sub = search_keys_sub(init)

# theorical_ratio = ratio_equation_b1(alpha, 2*alpha, init['T1'] , init['TR'] )
# print(theorical_ratio.shape)
# plt.title('Sensitivity ratio DAM')
# plt.xlabel('alpha [°]')
# plt.ylabel('S(alpha)/S(2*alpha)')

# plt.plot(alpha, theorical_ratio)
# plt.show()
"""