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
#import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import nibabel as nib 
from scipy import stats
from skimage.restoration import denoise_nl_means, estimate_sigma
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression

# My libraries
from utils_own.b1_mapping import *
from parameters.initialization_b1map import *
from utils import openArrayImages, interpolateImage, prepareHeaderOS, getSSIM

from utils_own.model import * 
from utils_own.utils import * 


""" def showPolyN(pickle_file):
    dic = pickle.load( open(pickle_file, "rb" ) )
    print(dic.shape)


pickle_file = "/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-01-29/fit_lin_deg_8_masked.pickle"

showPolyN(pickle_file) """
# PATHS

output_dir = "/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/reception_profile/"
path_transmission_profile =["/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/phantom_1/result_carte_b1_sub-001_fit_pol8.nii"]
#path_base_reception_profile = "/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/2021-02-10/reception_profile/meas_MID102_reception_profile_{0}_12-5_mM.nii" 
path_base_reception_profile_abs = "/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID102_31P_MT_cATP_FA0_PCr_VA24_FID19045_filter_hamming2_freq_0_echo_0_reception_profile_{0}_abs.nii" 
path_base_reception_profile_phase = "/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-02-10/reception_profile/meas_MID102_31P_MT_cATP_FA0_PCr_VA24_FID19045_filter_hamming2_freq_0_echo_0_reception_profile_{0}_phase.nii" 
mask_path = "/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Phantom/mask_opened_3.tif" 

# PARAMETER
N_channels = 8
os_factor = 2  
degres_poly = 5

 #path_reception_profile = getReceptionPaths(path_base_reception_profile,N_channels)
path_reception_profile_abs = getReceptionPaths(path_base_reception_profile_abs,N_channels)
path_reception_profile_phase = getReceptionPaths(path_base_reception_profile_phase,N_channels)
path_reception_profile_abs_fit = [] 
path_reception_profile_phase_fit = [] 

# Open images
B1_transmission = np.squeeze(openArrayImages(path_transmission_profile))
B1_reception_abs = openArrayImages(path_reception_profile_abs)
B1_reception_phase = openArrayImages(path_reception_profile_phase)


# Treating images fit poly
for i in range(N_channels):
    vol = np.squeeze(B1_reception_abs[i,:,:,:]) 
    img = nib.Nifti1Image(imageFitPolyN(vol,degres_poly,output_dir ), np.eye(4))
    path_reception_profile_abs_fit.append(os.path.join(output_dir,"result_carte_sensibility_ch{0}__fit_pol{1}.nii".format(i+1,degres_poly)))
    nib.save(img, path_reception_profile_abs_fit[i] )

B1_reception_abs_fit = openArrayImages(path_reception_profile_abs_fit)
B1_reception = B1_reception_abs_fit *np.exp(1j*B1_reception_phase)
B1_shape = B1_transmission.shape
B1_minus_shape = B1_reception.shape

B1_reception_int = np.zeros((B1_minus_shape[0],B1_minus_shape[1]*os_factor, B1_minus_shape[2]*os_factor, B1_minus_shape[3]*os_factor), complex)
for i in range(B1_minus_shape[0]):
        B1_reception_int[i,:,:,:]  = interpolateImage(B1_reception[i,:,:,:] , os_factor)

N_samples = B1_shape[0] * B1_shape[1] * B1_shape[2]

# Treating mask to make weights
mask = np.squeeze(openArrayImages(mask_path))
mask = mask /np.max(mask)
weights = mask.reshape(-1)

# Masking reception fields 
B1_reception_masked = np.zeros(B1_reception_int.shape, complex)# np.zeros((B1_shape[0],B1_shape[1],B1_shape[2],N_channels))
X =  np.zeros((N_samples, N_channels),complex)
for i in range(N_channels):
    B1_reception_masked[i,:,:,:] = mask*B1_reception_int[i,:,:,:]
    X[:,i] =  (B1_reception_masked[i,:,:,:]).reshape(-1)

# Fit transmission fit 
y = B1_transmission.reshape(-1)

reg = LinearRegression().fit(np.abs(X), y)
#reg_imag = LinearRegression().fit(np.imag(X), np.zeros(y))
print(reg.score(np.abs(X), y), reg.coef_, reg.intercept_)
#print(reg.score(X_real, y), reg.coef_, reg.intercept_)

y_fitted = reg.predict(np.abs(X)) 
print(y_fitted.shape)

B1_reception_fitted = y_fitted.reshape(B1_transmission.shape)
print(np.sum(y_fitted - y))

#nii = nib.load(path_transmission_profile[0]) 
img = nib.Nifti1Image(B1_reception_fitted,  np.eye(4))
nib.save(img,os.path.join(output_dir,"fitted_reception_profile.nii" ))




