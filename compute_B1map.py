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
from skimage.restoration import denoise_nl_means, estimate_sigma

# My libraries
from utils_own.b1_mapping import *
from utils import openArrayImages

init = INITIALIZATION['b1_database_phantom'] 


# Simulating data
S0 = 1
N_iterations = 1000


# True values
# Noise

"""alpha_0 = np.linspace(0, 45, num=15) # np.array([25,35,45] )
results_monte_carlo = np.zeros((alpha_0.size,N_iterations))
for j in range(alpha_0.size):
    S_alpha = equation_B1(init['T1'] ,init['TR'],get_sequence_alpha(alpha_0[j] ) , S0)
    std = 0.2*np.max(S_alpha ) 
    mean = 1*np.max(S_alpha ) 
    noise =  std * np.random.randn(S_alpha.size,N_iterations) + mean

    for i in range(N_iterations):
        y_obs = S_alpha +noise[:,i]
        x_values =[ init['T1'] ,init['TR']]
        for k in range(len(y_obs)):
            x_values.append(y_obs[k] )
        pop, _ = curve_fit(function_B1_double,
                                x_values,
                                y_obs,
                                maxfev=600)
                                
        results_monte_carlo[j,i] = pop # , a = pop #
#plt.plot(get_sequence_alpha(results_monte_carlo).T)   
plt.plot(alpha_0, alpha_0, '-', label='Ground truth' )#
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1), '-', label='Mean' )#
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1)+np.std(results_monte_carlo,axis=1), label='m + std')
plt.plot(alpha_0, np.mean(results_monte_carlo,axis=1)-np.std(results_monte_carlo,axis=1), label='m - std')
plt.legend()
#plt.plot(get_sequence_alpha(alpha_0), results_monte_carlo)
plt.show()
"""

#idx_courone = [8,10,13] 
idx_courone = [14,10,13] 


# REAL DATA
keys_sub = search_keys_sub(init)
for sub in keys_sub:
    SFdata = openArrayImages(init[sub])
    shape = SFdata.shape
    # FITT
    SFdata_denoised = np.zeros(shape)
    y_values = yFromSFdata(SFdata)
    
    results = np.zeros(y_values[:,0].shape)
    patch_size = 5
    patch_distance = 6
    sigma_est = np.mean(estimate_sigma(SFdata[0,:,:,:], multichannel=False))
    print(sigma_est)
    patch_kw = dict(patch_size=patch_size,      # 5x5 patches
                patch_distance=patch_distance)
   
    # fast algorithm, sigma provided
    for i in range(shape[0]):
        SFdata_denoised[i,:,:,:]  = denoise_nl_means(SFdata[i,:,:,:], h=0.6 * sigma_est, sigma=sigma_est,
                                    fast_mode=True, **patch_kw)  
        img = nib.Nifti1Image(np.squeeze(SFdata_denoised[i,:,:,:]), np.eye(4))
                                
        nib.save(img, "filter_nlm_patch_size_"+str(patch_size)+"_patch_distance_"+str(patch_distance)+"_img_"+str(i)+".nii")
    
    y_values_denoised = yFromSFdata(SFdata_denoised)
   # y_values = y_values_denoised
    for i in range(len(y_values[:,0])):
        x_values =[ init['T1'] ,init['TR']]
        for k in range(len(y_values[i,:])):
            x_values.append(y_values[i,k] )
        try:
            pop, _ = curve_fit(function_B1_double,
                                    x_values,
                                    y_values[i,:]  )
        
        except RuntimeError:
            results[i] = -1  
            pass
     #   print(y_values[i,:],results[i])
        results[i]= pop #
             
    array = results.reshape((shape[1], shape[2], shape[3]))
    img = nib.Nifti1Image(np.squeeze(array), np.eye(4))
    nib.save(img, "result_carte_b1_"+sub+"_den_patch_size_"+str(patch_size)+"_patch_distance_"+str(patch_distance)+".nii")

    alpha_estim = array[idx_courone[0] , idx_courone[1], idx_courone[2]  ] 
    s_obs =   SFdata[:,idx_courone[0],idx_courone[1],idx_courone[2] ] 
    s_obs_deno =   SFdata_denoised[:,idx_courone[0],idx_courone[1],idx_courone[2] ] 
    print(s_obs, s_obs_deno)
    alphas = get_sequence_alpha(alpha_estim)
    s_estimate = equation_B1(init['T1'] ,init['TR'], alphas, 1)
    den = np.sum(np.power(s_estimate,2))
    num = np.sum(s_obs*s_estimate)
    S0 = num/den
    plt.title('Signal ')
    plt.xlabel('alpha [°]')
    plt.plot(alphas, s_obs, 'gx', label='S_measure')
    plt.plot(alphas, s_obs_deno, 'rx',label='S_measure_den')
    alpha_fit = np.linspace(1,65,65)
    plt.plot(alpha_fit,  equation_B1(init['T1'] ,
                                        init['TR'],
                                        alpha_fit, 1)*S0,
                                        'b', label='S_fit')
    plt.legend()
    plt.show()

# alpha = np.arange(90)
# keys_sub = search_keys_sub(init)#

#plt.title('Sensitivity ratio DAM')
# plt.xlabel('alpha [°]')
# plt.ylabel('S(alpha)/S(2*alpha)')
#plt.plot(alpha, theorical_ratio)
# plt.show()
