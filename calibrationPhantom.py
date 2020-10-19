# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 15:33:54 2020

@author: RP258738, renata.porciunculabaptista@cea.fr

This script FID .dat


"""
import numpy as np
import pandas as pd
import sys, os
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pydicom

sys.path.append(os.path.join(sys.path[0],'./parameters/'))
sys.path.append(os.path.join(sys.path[0],'./utils_own/'))

from parameters.initialization_phantom import INITIALIZATION
from utils_own.model import signal_equation

phantom = INITIALIZATION['phantom_uniform']
peaks = np.zeros((len(phantom['TR'])))
peaks_fid = np.zeros((len(phantom['TR'])))
FA = np.asarray(phantom['FA'])
TR = np.asarray(phantom['TR'])

data = pd.read_excel(phantom['excel'], sheet_name='Results', na_rep='')
peaks_fid = data['mean_module']   
print(peaks_fid)
#Data
plt.plot(TR, peaks_fid, '+', label='data')

# Fit naive
popt, pcov = curve_fit(signal_equation, TR, peaks_fid,  bounds=([0, -np.inf, 0], [np.inf, np.inf,np.inf]))
plt.plot(TR, signal_equation(TR, *popt), 'r-',
         label='fit wo priori: M0=%5.3f, FA=%5.3f deg, T1=%5.3f ms' % tuple(popt))

# Fit with priore
popt, pcov = curve_fit(signal_equation, TR, peaks_fid, bounds=([0, 30, 2500], [1600, 120., 10000]))
plt.plot(TR, signal_equation(TR, *popt), 'g--',
         label='fit w/ priori: M0=%5.3f, FA=%5.3f deg, T1=%5.3f ms' % tuple(popt))

plt.xlabel('TR (ms)')
plt.ylabel('Peak of Fid')
plt.legend()
plt.show()
