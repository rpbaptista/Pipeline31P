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

# My libraries
from utils_own.b1_mapping import *
from parameters.initialization_b1map import *
from utils import openArrayImages, interpolateImage, prepareHeaderOS, getSSIM
spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])
from sklearn.metrics import plot_confusion_matrix

data = INITIALIZATION_B1['b1_database'] 
init = INITIALIZATION_B1


paths = ['/neurospin/ciclops/people/Renata/Meetings/metric/2021-03-12/rXFL_compare_5.nii',
 '/neurospin/ciclops/people/Renata/Meetings/metric/2021-03-12/rrresult_carte_b1_phantom-00-16_slice_2.nii',
 '/neurospin/ciclops/people/Renata/Meetings/metric/2021-03-12/mask.nii']

images = openArrayImages(paths) 
mask = np.squeeze(images[2,:,:]/np.max(images[2,:,:]))
image_xfl = np.squeeze(images[0,:,:])*mask 
image_avfa = np.squeeze(images[1,:,:])*mask

x = image_xfl.flatten()
y =  image_avfa.flatten()
res =  stats.linregress(x, y)

y_fitted = x*res.slope+res.intercept
print("slope",res.slope, "intercept", res.intercept)
plt.plot(x, y,'o',label='XFL data')
plt.plot(x, y_fitted,'r',label='fitted line')
plt.ylabel('M0 / mM')
plt.xlabel('FA map')
plt.legend()
plt.show()

print(res)