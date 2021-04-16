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
from parameters.initialization_1H import *
from utils import openArrayImages, interpolateImage, prepareHeaderOS, getSSIM
spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])
from sklearn.metrics import plot_confusion_matrix

data = INITIALIZATION_1H['b1_database_phantom_1H'] 
init = INITIALIZATION_1H

# Simulating data

# REAL DATA
keys_sub = search_keys_sub(data)
print("Compute individual maps")

#keys_sub =["sub-01","sub-02","sub-03","sub-04"] 
#keys_sub =["sub-04"] 

for sub in keys_sub:
    print("-----------"+sub)

    SFdata_aux = openArrayImages(data[sub])
    nii = nib.load(data[sub][0]) 
    y_values = yFromSFdata(SFdata_aux)
    results, err = T1mapFromYvalues(y_values, data)
    shape = SFdata_aux.shape
    # Saving T1 map 
    array = results[:,0].reshape((shape[1], shape[2]))
    img = nib.Nifti1Image(np.squeeze(array),  None, header=nii.header)
    nib.save(img, os.path.join(init['output_dir'][sub],"T1map.nii"))



