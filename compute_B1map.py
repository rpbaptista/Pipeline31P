# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""
# Systems libraries
import sys, os

sys.path.append(os.path.join(sys.path[0],'../Utils/'))
sys.path.append(os.path.join(sys.path[0],'./parameters/'))

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import nibabel as nib 
from scipy import stats
from skimage.restoration import denoise_nl_means, estimate_sigma


# My libraries
from utils_own.b1_mapping import *
from parameters.initialization_b1map import *
from utils import openArrayImages, interpolateImage
spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])

data = INITIALIZATION_B1['b1_database_phantom'] 
init = INITIALIZATION_B1

# Simulating data

#idx_courone = [8,10,13] 
#idx_courone = [14,10,13] 

idx_courone = [9,6,9] 
RUN_INDIVIDUAL = True


DENOISE = init['par_postproce']['DENOISE'] 
os_factor = init['par_postproce']['os_factor'] 

# REAL DATA
keys_sub = search_keys_sub(data)
print("Compute individual maps")

for sub in keys_sub:
    print("-----------"+sub)

    SFdata_aux = openArrayImages(data[sub])
    shape_aux = SFdata_aux.shape
    mask_aux = openArrayImages(init['mask'][sub])

    SFdata = np.zeros((shape_aux[0],shape_aux[1]*os_factor, shape_aux[2]*os_factor, shape_aux[3]*os_factor))
    mask = np.zeros((mask_aux.shape[0],shape_aux[1]*os_factor, shape_aux[2]*os_factor, shape_aux[3]*os_factor))
    for i in range(shape_aux[0] ):
        SFdata[i,:,:,:]  = interpolateImage(SFdata_aux[i,:,:,:] , os_factor)
    for i in range(mask_aux.shape[0]):
        mask[i,:,:,:]  = interpolateImage(mask_aux[i,:,:,:] , os_factor)
    shape = SFdata.shape
    # FITT
    SFdata_denoised = np.zeros(shape)
    y_values = yFromSFdata(SFdata)
    
   
    patch_size = init['par_postproce']['patch_size'] 
    patch_distance = init['par_postproce']['patch_distance'] 
    degres_poly = init['par_postproce']['deg_poly'] 

    sigma_est = np.mean(estimate_sigma(SFdata[0,:,:,0], multichannel=False))
    patch_kw = dict(patch_size=patch_size,      # 5x5 patches
                patch_distance=patch_distance)
    
    if DENOISE == True:
        y_values_denoised = yFromSFdata(SFdata_denoised)
        y_values = y_values_denoised# .copy()
   
    # generate strings name  
    filename_output,filename_fit_output, error_output = getFilenameB1(sub,init,DENOISE)
    
    # fast algorithm, sigma provided
    for i in range(shape[0]):
        SFdata_denoised[i,:,:,:]  = denoise_nl_means(SFdata[i,:,:,:], h=0.6 * sigma_est, sigma=sigma_est,
                                    fast_mode=True, **patch_kw)  
        img = nib.Nifti1Image(np.squeeze(SFdata_denoised[i,:,:,:]), np.eye(4))
                                
        nib.save(img,os.path.join(init['output_dir'][sub],"filter_nlm_patch_size_"+str(patch_size)+"_patch_distance_"+str(patch_distance)+"_img_"+str(i)+".nii"))
    
  

    if RUN_INDIVIDUAL == True:
        results, err = B1mapFromYvalues(y_values, data)

        # Saving B1 map 
        array = results.reshape((shape[1], shape[2], shape[3]))
        img = nib.Nifti1Image(np.squeeze(array), np.eye(4))
        nib.save(img, os.path.join(init['output_dir'][sub],filename_output))

        # Saving B1 error map
        error_ = err.reshape((shape[1], shape[2], shape[3]))
        img = nib.Nifti1Image(np.squeeze(error_), np.eye(4))
        nib.save(img,  os.path.join(init['output_dir'][sub],error_output))
        
        # Saving B1 map + poluy
        mask =np.squeeze(mask)

        img = nib.Nifti1Image(imageFitPolyN(np.squeeze(array),degres_poly,init['output_dir'][sub],mask  ), np.eye(4))
        nib.save(img, os.path.join(init['output_dir'][sub],filename_fit_output))
        

print("Compute average map")
for sub in keys_sub:
    imageToMNI(init['template']['mni'] ,init['anat'][sub], filename_output, init['output_dir'][sub])