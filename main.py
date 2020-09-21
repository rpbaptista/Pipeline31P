# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738, renata.porciunculabaptista@cea.fr

This script takes MT 31P MRI data and compute ratio in regions of interested

Dependencies:
 - spm standalone + MCR https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/glnxa64/
 - or Maltab + SPM
"""

import numpy as np
import nibabel as nib
import sys, os
import ants
import pandas as pd
from nipype.interfaces import spm

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append(os.path.join(sys.path[0],'../Utils/'))
sys.path.append(os.path.join(sys.path[0],'./libs/'))
sys.path.append(os.path.join(sys.path[0],'./parameters/'))

    
# Import homemade
#from metrics import statisticsImage
from utils import openArrayImages, createPath, createPathArray, saveArrayNifti
#from utilsEval import generateSaveGraphIntensityFA, computeStatistics
from parameters.initialization import INITIALIZATION
from utils_own.utils import *
from nipype import config
from nipype.interfaces import spm
import os

# Set SPM path
#matlab_cmd = '/volatile/softwares/standalone_spm/spm12/run_spm12.sh /volatile/softwares/MATLAB/MATLAB_Compiler_Runtime/v713/ script'
#spm.SPMCommand.set_mlab_paths(matlab_cmd=matlab_cmd, use_mcr=True)
spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])

# Initializations
sub_path = INITIALIZATION['paths']

atlas_subcortical = nib.load(INITIALIZATION['atlas']['path_sub']).get_fdata()
atlas_cortical = nib.load(INITIALIZATION['atlas']['path_cor']).get_fdata()


labels_cor = get_labels(INITIALIZATION['atlas'], 'labels_cor-xml')
labels_sub = get_labels(INITIALIZATION['atlas'], 'labels_sub-xml')

print("-- 31P MT pipeline  - v1.0--")


# Grouping mask to obtain the region of interest   
roi = aggregate_mask(INITIALIZATION['roi']['cortical'],  atlas_cortical)

# now, that I have the final mask I need to 
print("-Loading images-")

anat_1H_path = createPath(sub_path['anat_1H'],sub_path['subject_dir'] )
anat_31P_path = createPath(sub_path['anat_31P'],sub_path['subject_dir'] )

img_PCr = openArrayImages(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'])
img_cATP = openArrayImages(INITIALIZATION['paths']['31P_cATP'], sub_path['subject_dir'])

print("-Filter images: PCr images-")

img_filter_PCr = median_filter_images(img_PCr)

output_original_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'])
output_filter_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['meas', 'measFilter'])

print("-Saved filter images-")
saveArrayNifti(img_filter_PCr,output_path_PCr)

print("-Realing images-")
#realign_imgs(output_path_PCr)
calc_coreg_imgs(output_filter_path_PCr[0], output_filter_path_PCr[1:-1], 'output/pcr_toall.mat')

#print("-Find matrix images-")
#matrix = find_realign_matrix(os.path.split(output_path_PCr[0])[0])

print("-Apply transformation images")
apply_coreg_imgs(output_original_path_PCr[0], output_original_path_PCr[1:-1], 'output/pcr_toall.mat' )

print("--Sucess--")