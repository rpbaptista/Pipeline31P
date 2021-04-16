# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""
# Systems libraries
import sys, os

sys.path.append(os.path.join(sys.path[0],'../Utils/'))
sys.path.append(os.path.join(sys.path[0],'./parameters/'))
import sys, os 
import matplotlib.pyplot as plt
sys.path.append(os.path.join(sys.path[0],'./utils_own/'))

from utils_own.model import * 
from utils_own.bloch_equations import * 
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import nibabel as nib 
from scipy import stats
from skimage.restoration import denoise_nl_means, estimate_sigma
from metrics import *
from scipy import stats
# My libraries
from utils_own.b1_mapping import *
from parameters.initialization_b1map import *
from utils import openArrayImages, interpolateImage
from scipy import ndimage, misc

spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])

data =[ '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/phantom_1/phantom_mid122.nii',
      '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/phantom_1/phantom_md103.nii']  


init = INITIALIZATION_B1
keys_sub = search_keys_sub(INITIALIZATION_B1['b1_database_phantom'])

sub = keys_sub[0] 

mask_path = init['mask'][sub]
DENOISE = init['par_postproce']['DENOISE']
os_factor = init['par_postproce']['os_factor'] 

filename_output, filename_fit_output, error_output = getFilenameB1(sub,init,DENOISE)
b1_map_path =  os.path.join(init['output_dir'][sub],filename_fit_output)

concentration =[25,50] 
SFdata_aux = openArrayImages(data)
mask_aux = openArrayImages(mask_path)

b1_map = np.squeeze(openArrayImages(b1_map_path))

shape_aux = SFdata_aux.shape
SFdata = np.zeros((shape_aux[0],shape_aux[1]*os_factor, shape_aux[2]*os_factor, shape_aux[3]*os_factor))
mask = np.zeros((mask_aux.shape[0],shape_aux[1]*os_factor, shape_aux[2]*os_factor, shape_aux[3]*os_factor))
for i in range(shape_aux[0] ):
   SFdata[i,:,:,:]  = interpolateImage(SFdata_aux[i,:,:,:] , os_factor)
for i in range(mask_aux.shape[0] ):
   mask[i,:,:,:] = interpolateImage(mask_aux[i,:,:,:] , os_factor)

mask = np.squeeze(mask/np.max(mask))

shape_ = SFdata.shape
corrected = np.zeros((shape_[0],shape_[1] ,shape_[2],shape_[3]))
corrected_rec = np.zeros((shape_[1] ,shape_[2],shape_[3]))
fit_map = np.zeros((shape_[1] ,shape_[2],shape_[3]))


for i in range (shape_[1]):
    for j in range(shape_[2]):
        for k in range(shape_[3]):
            carte_b1 = b1_map[i,j,k]
            aux = signal_equation(0.25, 1,  carte_b1 , 6.7)/signal_equation(0.25, 1,  12.5 , 6.7)
            if np.abs(aux) < 1e-4:
               corrected[0,i,j,k] = -1
               corrected[1,i,j,k] = -1
            else:
               corrected[0,i,j,k] = SFdata[0,i,j,k]/aux
               corrected[1,i,j,k] = SFdata[1,i,j,k]/aux
            
    
corrected[corrected <= -0] = 0
mask = ndimage.binary_erosion(mask, structure=np.ones((5,5,5)))

# Create b1- map from 50mM, segunda imagem
B1_reception = (corrected[1,:,:,:] /concentration[1]) 
B1_reception = np.nan_to_num(B1_reception, nan=0)

img = nib.Nifti1Image(B1_reception *mask, np.eye(4))
nib.save(img, os.path.join(init['output_dir'][sub],'B1_map_reception_inversion.nii'))
img = nib.Nifti1Image(np.squeeze(corrected[0,:,:,:]/concentration[0])*mask, np.eye(4))
nib.save(img, os.path.join(init['output_dir'][sub],'corrected_25mM_transmission_only.nii'))

img = nib.Nifti1Image(np.squeeze(corrected[1,:,:,:]/concentration[1])*mask, np.eye(4))
nib.save(img, os.path.join(init['output_dir'][sub],'corrected_50mM_transmission_only.nii'))


mask_erode = ndimage.binary_erosion(mask, structure=np.ones((4,4,4)))


correct_bothways = np.squeeze(corrected[0,:,:,:]/concentration[0])*(1/B1_reception)

img = nib.Nifti1Image(correct_bothways*mask, np.eye(4))
nib.save(img, os.path.join(init['output_dir'][sub],'corrected_25mM_transmission_reception_inversion.nii'))

img = nib.Nifti1Image(np.squeeze(corrected[1,:,:,:]/concentration[1])*mask/B1_reception, np.eye(4))
nib.save(img, os.path.join(init['output_dir'][sub],'corrected_50mM_transmission_reception_inversion.nii'))

y = maskImageToArray(np.squeeze(corrected[1,:,:,:]/concentration[1]),mask_erode)
x = maskImageToArray(b1_map,mask_erode)


res =  stats.linregress(x, y)

B1_reception_k = (b1_map*res.slope+res.intercept)
img = nib.Nifti1Image(B1_reception_k *mask, np.eye(4))
nib.save(img, os.path.join(init['output_dir'][sub],'B1_map_reception_prop.nii'))
correct_bothways_ = np.squeeze(corrected[0,:,:,:]/concentration[0])*(1/B1_reception_k)

img = nib.Nifti1Image(correct_bothways_*mask, np.eye(4))
nib.save(img, os.path.join(init['output_dir'][sub],'corrected_25mM_transmission_reception_kproportional.nii'))

correct_bothways_ = np.squeeze(corrected[1,:,:,:]/concentration[1])*(1/B1_reception_k)

img = nib.Nifti1Image(correct_bothways_*mask, np.eye(4))
nib.save(img, os.path.join(init['output_dir'][sub],'corrected_50mM_transmission_reception_kproportional.nii'))

#x_full = np.arange(x.min(),x.max(),200)
y_fitted = x*res.slope+res.intercept
print("slope",res.slope, "intercept", res.intercept)
plt.plot(x, y,'o',label='original data')
plt.plot(x, y_fitted,'r',label='fitted line')
plt.ylabel('M0 / mM')
plt.xlabel('FA map')
plt.legend()
plt.show()
print(res.rvalue)

# 

