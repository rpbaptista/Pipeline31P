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

INITIALIZATION['b1_database'] = {
    'sub-01' : ['/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-14/meas_MID236_31P_MT_cATP_FA0_PCr_VA50_FID16096_filter_hamming2_freq_0_echo_0.nii',
                '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Phantom/2021-01-14/meas_MID237_31P_MT_cATP_FA0_PCr_VA25_FID16097_filter_hamming2_freq_0_echo_0.nii'],
    'FA_nominal' : [25,50],
    'T1' : 3.37,
    'TR' : 0.250,
}

def function_alpha(x_values, S0, alpha):
    T1 = x_values[0]
    TR = x_values[1]

    ans = equation_B1(T1, TR, alpha, alpha*2, S0)
    return ans
def equation_B1(T1, TR, alpha_1, alpha_2, S0=1):
    """
    DAM method no relaxed T1
    alpha_1 deg
    alpha_2 deg
    """
    S1 = signal_equation(TR, S0, alpha_1, T1)
    S2 = signal_equation(TR, S0, alpha_2, T1)
    
    return S1/S2

def search_keys_sub(dict_b1_database):
    result = []

    for key in dict_b1_database:
        if key.startswith('sub-'):
            result.append(key)   
    return result

def ratio_image(SFData):
    return np.squeeze(SFData[0,:,:,:]/SFData[1,:,:,:])