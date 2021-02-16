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

data =[ '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/Test_correction/2021-02-10/result_carte_b1_sub-001.nii',
 '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/meas_MID122_31P_MT_cATP_FA0_PCr_VA12_FID19065_filter_hamming2_freq_0_echo_0.nii',
 '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/Test_correction/2021-02-10/mask_more_conservative.nii']  

#data =[ '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/Test_correction/result_carte_b1_phantom-00-filter-median.nii',
# '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/Test_correction/meas_MID236_31P_MT_cATP_FA0_PCr_VA50_FID16096_filter_hamming2_freq_0_echo_0.nii'] 
os_factor = 2

SFdata_aux = np.squeeze(openArrayImages(data))
shape_aux = SFdata_aux.shape
SFdata = np.zeros((shape_aux[0],shape_aux[1]*os_factor, shape_aux[2]*os_factor, shape_aux[3]*os_factor))
for i in range(shape_aux[0]-1 ):
   SFdata[0,:,:,:]  = SFdata_aux[0,:,:,:]
   SFdata[i+1,:,:,:]  = interpolateImage(SFdata_aux[i+1,:,:,:] , os_factor)

mask = np.squeeze(SFdata[2,:,:,:]/np.max(SFdata[2,:,:,:]))

shape_ = SFdata.shape

corrected = np.zeros((shape_[1] ,shape_[2],shape_[3]))
fit_map = np.zeros((shape_[1] ,shape_[2],shape_[3]))


for i in range (shape_[1]):
    for j in range(shape_[2]):
        for k in range(shape_[3]):
           # carte_b1 = ndimage.median_filter(SFdata[0,i,j,k], size=4)
            carte_b1 = SFdata[0,i,j,k]
            image = SFdata[1,i,j,k]

         #   aux = signal_equation(0.25, 1, 50 , 6.7)/signal_equation(0.25, 1, 50/12* carte_b1 , 6.7)
            aux = signal_equation(0.25, 1,  carte_b1 , 6.7)
            if np.abs(aux) < 1e-5:
               print(aux)
               corrected[i,j,k] = 0
            else:
               corrected[i,j,k] = image/aux
       #  polynomial_coeff=np.polyfit(x,y,2)       
         #   print(aux, image)
corrected[corrected < 0] = 0
img = nib.Nifti1Image(corrected, np.eye(4))
nib.save(img, 'corrected_25mM.nii')


img = nib.Nifti1Image(corrected/25, np.eye(4))
nib.save(img, 'corrected_25mM_under_concentration.nii')

x = maskImageToArray(corrected/25.0,mask)
y = maskImageToArray(SFdata[0,:,:,:],mask)

# corr = np.correlate(x,y)
# corr
print(x.shape, y.shape)
slope, intercept, r, p, se =  stats.linregress(x, y)
print(r)
plt.plot(x,y,'o')
x_full = np.arange(x.min(),x.max(),200)
plt.plot(x_full, x_full*slope+intercept)
plt.ylabel('M0 / mM')
plt.xlabel('FA map')
plt.show()