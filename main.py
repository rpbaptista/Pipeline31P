# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738, renata.porciunculabaptista@cea.fr

This script takes MT 31P MRI data and compute ratio in regions of interested

Dependencies:
 - spm standalone + MCR https://www.fil.ion.ucl.ac.uk/spm/download/restricted/utopia/MCR/glnxa64/
 - or Maltab + SPM
"""

import argparse
import numpy as np
import nibabel as nib
import sys, os
import ants
import pandas as pd
from nipype.interfaces import spm
from nipype import config

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
from metrics import statisticsImage

# Set SPM path
#matlab_cmd = '/volatile/softwares/standalone_spm/spm12/run_spm12.sh /volatile/softwares/MATLAB/MATLAB_Compiler_Runtime/v713/ script'
#spm.SPMCommand.set_mlab_paths(matlab_cmd=matlab_cmd, use_mcr=True)
spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])


if __name__ == '__main__':
    # Treat arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--align31P",
                        help="0/1 to do first step analysis",
                        type=int,
                        default = 0)
                        
    parser.add_argument("--alignAnat",
                        help="0/1 to do second step analysis",
                        type=int,
                        default = 0)
    
    parser.add_argument("--warpMNI",
                        help="0/1 to do third step analysis",
                        type=int,
                        default = 0)

    parser.add_argument("--createROI",
                        help="0/1 to do four step analysis",
                        type=int,
                        default = 1)
    
    parser.add_argument("--computeStatistics",
                        help="0/1 to do four step analysis",
                        type=int,
                        default = 1)

  
    args = parser.parse_args()

    sub_path = INITIALIZATION['paths']

    atlas_subcortical = nib.load(INITIALIZATION['atlas']['path_sub']).get_fdata()
    atlas_cortical = nib.load(INITIALIZATION['atlas']['path_cor']).get_fdata()


    labels_cor = get_labels(INITIALIZATION['atlas'], 'labels_cor-xml')
    labels_sub = get_labels(INITIALIZATION['atlas'], 'labels_sub-xml')

    print("--------- 31P MT pipeline  - v1.0------------")

    # now, that I have the final mask I need to 
    print("-Load images")

    anat_1H_path = createPath(sub_path['anat_1H'],sub_path['subject_dir'] )
    realign_MNI_anat_1H_path = createPath(sub_path['anat_1H'],sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'])
    anat_31P_path = createPath(sub_path['anat_31P'],sub_path['subject_dir'] )
    realign_31P_anat_path = createPath(sub_path['anat_31P'],sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'])
    #Final
    resliced_1H_MNI = add_prefix(realign_MNI_anat_1H_path, 'r')
    resliced_31P_into_MNI_1H = add_prefix(realign_31P_anat_path, 'r')

    warp_file = resliced_1H_MNI.replace('.nii', '_warpcoef.nii.gz')

    img_PCr = openArrayImages(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'])
    nii = nib.load(createPath(INITIALIZATION['paths']['31P_PCr'][0], sub_path['subject_dir']))
    header = nii.header
    img_cATP = openArrayImages(INITIALIZATION['paths']['31P_cATP'], sub_path['subject_dir'])
    # Processed mask
    mask_volunteer = createPath( 'mask_volunteer.nii',sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'])


    # Original images
    output_original_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'])
    output_original_path_cATP = createPathArray(INITIALIZATION['paths']['31P_cATP'], sub_path['subject_dir'])

    # Processed images
    output_filter_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['meas', 'measFilter'])
    output_filter_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['meas', 'measFilter'])

    output_realignfilter_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['meas', 'measrealfilter'])
    output_realign_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['meas', 'rmeas'])
    output_realign_path_cATP = createPathArray(INITIALIZATION['paths']['31P_cATP'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['meas', 'rmeas'])
    final_realign_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['meas', 'final_meas'])
    final_realign_path_cATP = createPathArray(INITIALIZATION['paths']['31P_cATP'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['meas', 'final_meas'])

    output_anat_realign_path_PCr = createPathArray(INITIALIZATION['paths']['31P_PCr'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['rmeas', 'anatrmeas'])
    output_anat_realign_path_cATP = createPathArray(INITIALIZATION['paths']['31P_cATP'], sub_path['subject_dir'], INITIALIZATION['paths']['replaceFolder'], ['rmeas', 'anatrmeas'])

    if (args.align31P == 1):
        print("-Register all 31P")

        print("--Filter images: PCr images...")
        img_filter_PCr = median_filter_images(img_PCr)

        print("--Saved filter images...")
        saveArrayNifti(img_filter_PCr,output_filter_path_PCr, header)

        print("--Realing images...")
        #realign_imgs(output_path_PCr)
        calc_coreg_imgs(output_filter_path_PCr[0], output_filter_path_PCr, '/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/pcr_toall.mat')

        print("--Apply transformation images...")
        apply_transf_imgs(output_filter_path_PCr, '/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/pcr_toall.mat' , output_realignfilter_path_PCr)
        apply_transf_imgs(output_original_path_PCr, '/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/pcr_toall.mat' , output_realign_path_PCr)
        apply_transf_imgs(output_original_path_cATP, '/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/pcr_toall.mat' , output_realign_path_cATP)
    else:
        print("-Skipped aligned with 31P images.")

    if (args.alignAnat == 1):

        print("-Register and reslice with anatomy")
        
        print("--Realigned anat to TEMPLATE")
        calc_coreg_imgs(INITIALIZATION['template']['mni'], [anat_1H_path], '/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/anat_register_mni.mat')
        apply_transf_imgs([anat_1H_path], '/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/inverse_anat_register_mni.mat' , [realign_MNI_anat_1H_path])

        print("--Reslice anat 1H into MNI")
        reslice(INITIALIZATION['template']['mni'], realign_MNI_anat_1H_path)


        print("--Realigned anat 31 P to anat-1H-MNI")
        calc_coreg_imgs(resliced_1H_MNI, [anat_31P_path], '/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/anat1H_anat31P.mat')
        apply_transf_imgs([anat_31P_path], '/neurospin/ciclops/people/Renata/Codes/Pipeline31P/output/inverse_anat1H_anat31P.mat' , [realign_31P_anat_path])

        print("--Reslice anat 1H into MNI")
        reslice(resliced_1H_MNI, realign_31P_anat_path)


        print("--Realigned 31 P to anat 31P-1H-MNI")
        coreg_imgs(resliced_31P_into_MNI_1H, output_realignfilter_path_PCr, output_realign_path_PCr,output_realign_path_cATP, 'anat31Pr')
    
    else:
        print("-Skipped aligned with anat.")

    if (args.warpMNI == 1):
        print("-Finding inverse transformation anat -> MNI")
        print("--FNIRT")
        normalize_out = normalize(resliced_1H_MNI, INITIALIZATION['template']['mni'])

        print("--Compute Inverse ")
        inv_warp(warp_file,resliced_1H_MNI)

    else:
        print("-Skipped inverse transformation anat -> MNI")

    if (args.createROI == 1):
        print("-Create individual ROI")
        print("--Create ROI in MNI")
        mask = aggregate_mask(INITIALIZATION['roi']['cortical'],  INITIALIZATION['atlas']['path_cor'], mask_volunteer)

        print("--Apply individual inverse transformation to MNI")
        apply_warp(mask_volunteer, INITIALIZATION['template']['mni'], warp_file)

    else:
        print("-Skipped create ROI MNI.")
    
    if (args.computeStatistics == 1):
        print("-Compute mean in ROI")
        r_final_realign_path_cATP = add_prefix(output_realign_path_cATP, 'anat31Pr')
        r_final_realign_path_PCr = add_prefix(output_realign_path_PCr, 'anat31Pr')
        
        vols_cATP = openArrayImages(r_final_realign_path_cATP)
        vols_PCr = openArrayImages(r_final_realign_path_PCr)
        mask_volunteer = openArrayImages(mask_volunteer)
        FA = INITIALIZATION['acquisition']['FA']
        FA = np.asarray(FA)

        mean_pcr = np.zeros(FA.shape)
        error_pcr = np.zeros(FA.shape)
        max_pcr = np.zeros(FA.shape)

        mean_catp = np.zeros(FA.shape)
        error_catp = np.zeros(FA.shape)
        max_catp = np.zeros(FA.shape)

        for i in range(img_cATP.shape[0]):
            stats_pcr = statisticsImage(vols_PCr[i,:,:,:], mask_volunteer)
            error_pcr[i] = stats_pcr.std
            mean_pcr[i] = stats_pcr.mean
            max_pcr[i] = stats_pcr.max

            stats_catp = statisticsImage(vols_cATP[i,:,:,:], mask_volunteer)
            error_catp[i] = stats_catp.std
            max_catp[i] = stats_catp.max
            mean_catp[i] = stats_catp.mean

        print(mean_catp)
        print(mean_pcr)

    else:
        print("-Skipped compute Statistics")


    print("--Sucess--")


