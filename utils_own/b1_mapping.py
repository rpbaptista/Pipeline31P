# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""

import numpy as np
import sys, os

sys.path.append(os.path.join(sys.path[0],'./utils_own/'))

from utils_own.model import * 

INITIALIZATION = dict()

INITIALIZATION['b1_database_phantom'] = {
    #   'sub-00' : ['/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID112_31P_MT_cATP_FA0_PCr_VA12_FID16768_filter_hamming2_freq_0_echo_0.nii',
 #               '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID110_31P_MT_cATP_FA0_PCr_VA24_FID16766_filter_hamming2_freq_0_echo_0.nii',
 #           '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID103_31P_MT_cATP_FA0_PCr_VA36_FID16759_filter_hamming2_freq_0_echo_0.nii',
 #           '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-20/meas_MID108_31P_MT_cATP_FA0_PCr_VA48_FID16764_filter_hamming2_freq_0_echo_0.nii'], 

'sub-01' : [
    '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-29/meas_MID634_31P_MT_cATP_FA0_PCr_VA24_FID17904_filter_hamming2_freq_0_echo_0.nii',
   '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-29/meas_MID633_31P_MT_cATP_FA0_PCr_VA48_FID17903_filter_hamming2_freq_0_echo_0.nii'], 

    'FA_nominal' : [12,24,36,48],
    'T1' : 6.7,
    'TR' : 0.250
    }
INITIALIZATION['b1_database'] = {
 'sub-01' : [
    '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2021-01-27/meas_MID468_31P_MT_cATP_FA0_PCr_VA12_FID17680_filter_hamming2_freq_0_echo_0.nii',
   '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2021-01-27/meas_MID467_31P_MT_cATP_FA0_PCr_VA24_FID17679_filter_hamming2_freq_0_echo_0.nii',
'/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2021-01-27/meas_MID466_31P_MT_cATP_FA0_PCr_VA36_FID17678_filter_hamming2_freq_0_echo_0.nii',
    '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2021-01-27/meas_MID465_31P_MT_cATP_FA0_PCr_VA48_FID17677_filter_hamming2_freq_0_echo_0.nii'],

    'FA_nominal' : [12,24,36,48],
    'T1' : 3.37,
    'TR' : 0.250,
}
"""
def yFromSFdata(SFdata):
    y_values_alpha_1 = SFdata[0,:,:,:].reshape((-1,1))
    y_values_alpha_2 = SFdata[1,:,:,:].reshape((-1,1))
    return np.hstack((y_values_alpha_1 ,y_values_alpha_2))
def get_sequence_alpha(alpha):
    return np.array([alpha, 2*alpha]).flatten()
"""

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