import numpy as np
import math
import sys, os 
import matplotlib.pyplot as plt
sys.path.append(os.path.join(sys.path[0],'./utils_own/'))

from utils_own.model import * 
from scipy.optimize import curve_fit


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
    """
    print("... warning: considering T1 and T2")
    signal_under_concentration = signal/calib['true_value']
    M0_under_concentration = getM0fromSignal(signal= signal_under_concentration,
                        alpha_deg  = calib['FA'],
                        T1 = calib[in_met]['T1'],
                        TR = calib['TR']
                  #      T2 = calib[in_met]['T2'],
                   #     TE = calib['TE']
                   )
  #  M0_under_concentration = M0/calib['true_value']
    M0_under_concentration_times_T1_pond = signal_equation_T1_T2(TR = calib['TR'],
                                                 M0= M0_under_concentration,
                                                  alpha_deg=  calib['FA'],
                                                  T1=  calib[out_met]['T1'],
                                                  T2= calib[out_met]['T2e'],
                                                  TE= calib['TE'])
    return  M0_under_concentration_times_T1_pond