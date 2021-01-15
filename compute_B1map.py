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

# My libraries
from utils_own.b1_mapping import *
from utils import openArrayImages

init = INITIALIZATION['b1_database'] 

alpha = np.arange(45)
keys_sub = search_keys_sub(init)

count = 0
for sub in keys_sub:
    SFdata = openArrayImages(init[sub])
    if count == 0:
        shape = SFdata.shape
        subs_ratios = np.zeros((len(keys_sub),shape[1], shape[2], shape[3])) 
    subs_ratios[count,:,:,:]  = ratio_image(SFdata) 
    count = count + 1

y_values = subs_ratios.reshape((-1,1))

# curve fit
popt, _ = curve_fit(function_alpha,[init['T1'] ,init['TR']], y_values )
S0, alpha = popt

print(array.shape,array.mean, array.std, S0, alpha)
#  

print("Test",subs_ratios.shape)
img = nib.Nifti1Image(np.squeeze(subs_ratios[count-1,:,:,:]), np.eye(4))
nib.save(img, "result_carte_b1.nii")

theorical_ratio = equation_B1(alpha, 2*alpha, init['T1'] , init['TR'] )

plt.title('Sensitivity ratio DAM')
plt.xlabel('alpha [°]')
plt.ylabel('S(alpha)/S(2*alpha)')

plt.plot(alpha, theorical_ratio)
#plt.show()
