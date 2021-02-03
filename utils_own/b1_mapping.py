# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""

import numpy as np
import sys, os

sys.path.append(os.path.join(sys.path[0],'./utils_own/'))

from utils_own.model import * 
from utils_own.utils import * 
"""
def yFromSFdata(SFdata):
    y_values_alpha_1 = SFdata[0,:,:,:].reshape((-1,1))
    y_values_alpha_2 = SFdata[1,:,:,:].reshape((-1,1))
    return np.hstack((y_values_alpha_1 ,y_values_alpha_2))
def get_sequence_alpha(alpha):
    return np.array([alpha, 2*alpha]).flatten()
"""

def imageToMNI(template,anat,image, output_dir):
    print("--Realigned anat to TEMPLATE")
    calc_coreg_imgs(template, [anat], os.path.join(output_dir,'anat_register_mni.mat'))
    
    realign_anat = add_prefix(anat, 'r')
    resliced_1H_MNI = add_prefix(realign_anat, 'fsl_r')
    warp_file = resliced_1H_MNI.replace('.nii', '_warpcoef.nii')

    apply_transf_imgs([anat], os.path.join(output_dir,'inverse_anat_register_mni.mat') , [realign_anat])
    
    print("--Reslice anat 1H into MNI")
    reslice(template, realign_anat)
    aux = add_prefix(realign_anat, 'r')
    fsl_anat(aux, resliced_1H_MNI,0, warp_file,  warp_file.replace('.nii', '_inverse.nii'), template, brain=False)
    return 0


def B1mapFromYvalues(y_values,init):
    results = np.zeros(y_values[:,0].shape)
    err = np.zeros(y_values[:,0].shape)

    for i in range(len(y_values[:,0])):
        x_values =[ init['T1'] ,init['TR']]
        for k in range(len(y_values[i,:])):
            x_values.append(y_values[i,k] )
        try:
            pop, pcov = curve_fit(function_B1_double,
                                    x_values,
                                    y_values[i,:] ,absolute_sigma=True )
        #    print("parameters, pcov", pop, pcov)
        except RuntimeError:
            results[i] = -1  
            err[i] = -1 
            pass
     #   print(y_values[i,:],results[i])
        results[i]= pop #
        err[i]  = np.sqrt(np.diag(pcov))
    return results, err
def yFromSFdata(SFdata):
    y_values_alpha_1 = SFdata[0,:,:,:].reshape((-1,1))
    y_values_alpha_2 = SFdata[1,:,:,:].reshape((-1,1))
    y_values_alpha_3 = SFdata[2,:,:,:].reshape((-1,1))
    y_values_alpha_4 = SFdata[3,:,:,:].reshape((-1,1))
    return np.hstack((y_values_alpha_1 ,y_values_alpha_2,y_values_alpha_3,y_values_alpha_4))
def get_sequence_alpha(alpha):
    return np.array([alpha, 2*alpha, 3*alpha, 4*alpha]).flatten()

def function_B1_double(x_values, alpha):
    T1 = x_values[0]
    TR = x_values[1]
    y_obs =[]
    for i in range(len(x_values )-2):
        y_obs.append(x_values[i+2] ) 

    alphas = get_sequence_alpha(alpha)
    ans = equation_B1(T1, TR, alphas, 1)
    den = np.sum(np.power(ans,2))
    num = np.sum(y_obs*ans)
    S0 = num/den
    return ans*S0


def function_B1(x_values, S0, alpha):
    T1 = x_values[0]
    TR = x_values[1]
    ans = equation_B1(T1, TR, alpha,  S0)
    
    return ans

def equation_B1(T1, TR, alpha_1, S0=1):
    """
    DAM method no relaxed T1
    alpha_1 deg
    alpha_2 deg
    """
    S1 = signal_equation(TR, S0, alpha_1, T1)    
    return S1

# def ratio_equation_b1(T1, TR, alpha_1, alpha_2, S0=1):
#     """
#     DAM method no relaxed T1
#     alpha_1 deg
#     alpha_2 deg
#     """
#     S1 = signal_equation(TR, S0, alpha_1, T1)
#     S2 = signal_equation(TR, S0, alpha_2, T1)
    
    return S1/S2
def search_keys_sub(dict_b1_database):
    result = []

    for key in dict_b1_database:
        if key.startswith('sub-'):
            result.append(key)   
    return result

def ratio_image(SFData):
    return np.squeeze(SFData[0,:,:,:]/SFData[1,:,:,:])