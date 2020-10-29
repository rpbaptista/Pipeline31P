import numpy as np
import math
import sys, os 
import matplotlib.pyplot as plt
sys.path.append(os.path.join(sys.path[0],'./utils_own/'))

from utils_own.model import * 
from utils_own.bloch_equations import * 
from scipy.optimize import curve_fit

def getMSE(a,b):
    return np.sqrt(np.sum((a - b)**2))

def getKab(range_kab,ratio, Mobs_a, FA_sub, calib, nameA, nameB, Mobs_b=None):
    error = np.zeros(range_kab.shape)
    M0a = np.array([0,0,1])
    M0b = np.array([0,0,1/ratio])
    for i in range(range_kab.size):
        M_a, M_b = getTheoricalValues(range_kab[i],ratio*range_kab[i], M0a, M0b, FA_sub, calib, nameA, nameB)
        M_a = M_a/np.max(M_a)
        error[i] = getMSE(Mobs_a,M_a) + getMSE(Mobs_b,M_b)
    idx = np.argmin(error)
    return  range_kab[idx]

def getTheoricalValues(kab, kba, M0a, M0b, FA_sub, calib, nameA, nameB):
    w1b = getW1fromFAandTau(FA_sub, calib['tau'])
    M_a = np.zeros(FA_sub.shape)
    M_b = np.zeros(FA_sub.shape)
    for i in range(FA_sub.size):  
        A, C, M0 = getMagMat(0, 0, M0a, M0b, kab, kba, calib[nameA], calib[nameB], 0, w1b[i])
        A_without_sat, C_without_sat, M0_without_sat = getMagMat(0, 0, M0a, M0b, kab, kba, calib[nameA], calib[nameB], 0, 0)

        M = mag_signal_N(10, calib['FA'], calib['TE'], calib['TR'], calib['tau'] ,A, C, M0,A_without_sat)
        """plt.plot(np.sqrt(M[0,:]**2+M[1,:]**2), label = 'Az')
        plt.legend()
        plt.show()
        plt.plot(np.sqrt(M[3,:]**2+M[4,:]**2), label = 'Bz')
        plt.legend()
        plt.show()"""
        M_a[i] = np.sqrt(M[0,-1]**2+M[1,-1]**2)
        M_b[i] = np.sqrt(M[3,-1]**2+M[4,-1]**2)
    return M_a, M_b


def getKf(rangeK, Msreal, t, Mc, T1):
    error = np.zeros(rangeK.shape)
    for i in range(max(rangeK.shape)):
    #    print(getMs(t, Mc, T1, rangeK[i]), Msreal)
        error[i] = np.abs(Msreal - getMs(t, Mc, T1, rangeK[i]))
    ind = np.argmin(error)
    return rangeK[ind], error

def getMs(t, Mc, T1, Kf):
    Mt = equation_Mt_simp(Mc, t, T1, Kf)
    return Mt[-1]

def meanMask(image, mask):
    mask = mask/np.max(mask)
    mask = np.broadcast_to(mask, image.shape)
    array = image*mask
    array = array[array!=0]
    return  np.mean(array)

def getCoefficient (signal, calib, in_met, out_met):
    """
    Inputs: calib must be a dictionary with the keys true_value, fa, t1
    M0 = K* [concentration]
    S = M0 * pondT1T2
    """
    print("... warning: only considering T1")
    signal_under_concentration = signal/calib['true_value']
    K0 = getM0fromSignal(signal= signal_under_concentration,
                        alpha_deg  = calib['FA'],
                        T1 = calib[in_met]['T1'],
                        TR = calib['TR'])
  #  M0_under_concentration = M0/calib['true_value']
    K0_times_T1_pond = signal_equation(TR = calib['TR'],
                                                 M0= K0,
                                                 alpha_deg=  calib['FA'],
                                                 T1=  calib[out_met]['T1'])
    return  K0_times_T1_pond 

def getCoefficient_T1_T2 (signal, calib, in_met, out_met):
    """
    Inputs: calib must be a dictionary with the keys true_value, fa, t1
    M0 = K* [concentration]
    S = M0 * pondT1T2
    """

    print("... warning: considering T1 and T2")
    signal_under_concentration = signal/calib['true_value']
    M0_under_concentration = getM0fromSignal_T1_T2(signal= signal_under_concentration,
                        alpha_deg  = calib['FA'],
                        T1 = calib[in_met]['T1'],
                        TR = calib['TR'],
                        T2 = calib[in_met]['T2e'],
                        TE = calib['TE']
                   )
  #  M0_under_concentration = M0/calib['true_value']
    M0_under_concentration_times_T1_pond = signal_equation_T1_T2(TR = calib['TR'],
                                                 M0= M0_under_concentration,
                                                  alpha_deg=  calib['FA'],
                                                  T1=  calib[out_met]['T1'],
                                                  T2= calib[out_met]['T2e'],
                                                  TE= calib['TE'])
    return  M0_under_concentration_times_T1_pond