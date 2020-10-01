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
from utils import openArrayImages,createPath, openArrayImages, plotStatMT, createPathArray, createPathArray, saveArrayNifti
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
    parser.add_argument("--alignAnat",
                        help="0/1 to do second step analysis",
                        type=int,
                        default = 0) # This step is long and works really well no need to keep updating
    
    parser.add_argument("--align31P",
                        help="0/1 to do first step analysis",
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

    sub_par = INITIALIZATION['sub01']
    roi = INITIALIZATION['roi']['cortical_up']

    print("--------- 31P MT pipeline  - v1.0------------")

    # now, that I have the final mask I need to 
    print("-Load images")
    
    #Final
    anat_1H_path = createPath(sub_par['anat_1H'],sub_par['subject_dir'] )
    realign_MNI_anat_1H_path = createPath(sub_par['anat_1H'],sub_par['subject_dir'], sub_par['replaceFolder'])
    anat_31P_path = createPath(sub_par['anat_31P'],sub_par['subject_dir'] )
    realign_31P_anat_path = createPath(sub_par['anat_31P'],sub_par['subject_dir'], sub_par['replaceFolder'])

    resliced_1H_MNI = add_prefix(realign_MNI_anat_1H_path, 'r')
    resliced_31P_into_MNI_1H = add_prefix(realign_31P_anat_path, 'r')

    warp_file = resliced_1H_MNI.replace('.nii', '_warpcoef.nii.gz')

    img_PCr = openArrayImages(sub_par['31P_PCr'], sub_par['subject_dir'])
    nii = nib.load(createPath(sub_par['31P_PCr'][0], sub_par['subject_dir']))
    header = nii.header
    img_cATP = openArrayImages(sub_par['31P_cATP'], sub_par['subject_dir'])

    # Processed mask
    mask_volunteer = createPath( 'mask_volunteer.nii',sub_par['subject_dir'], sub_par['replaceFolder'])


    # Original images
    output_original_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'])
    output_original_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'])

    # Processed images
    output_filter_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'measFilter'])
    output_filter_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'measFilter'])

    output_realign_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'rmeas'])
    output_realign_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'rmeas'])

    if (args.alignAnat == 1):

        print("-Register and reslice with anatomy")
       
        print("--Realigned anat to TEMPLATE")
        calc_coreg_imgs(INITIALIZATION['template']['mni'], [anat_1H_path], os.path.join(sub_par['output_dir'],'anat_register_mni.mat'))
        apply_transf_imgs([anat_1H_path], os.path.join(sub_par['output_dir'],'inverse_anat_register_mni.mat') , [realign_MNI_anat_1H_path])

        print("--Reslice anat 1H into MNI")
        reslice(INITIALIZATION['template']['mni'], realign_MNI_anat_1H_path)

        print("--Realigned anat 31 P to anat-1H-MNI")
        calc_coreg_imgs(resliced_1H_MNI, [anat_31P_path], os.path.join(sub_par['output_dir'],'anat1H_anat31P.mat') )
        apply_transf_imgs([anat_31P_path], os.path.join(sub_par['output_dir'],'inverse_anat1H_anat31P.mat') , [realign_31P_anat_path])

        print("--Reslice anat 1H into MNI")
        reslice(resliced_1H_MNI, realign_31P_anat_path)
           
    else:
        print("-Skipped aligned with anat.")


    if (args.align31P == 1):
        print("-Aligned 31P to 31P-1H-MNI")

        print("--Filter images: PCr images...")
        img_filter_PCr = median_filter_images(img_PCr)
        img_filter_cATP = median_filter_images(img_cATP)

        print("--Saved filter images...")
        saveArrayNifti(img_filter_PCr,output_filter_path_PCr, header)
        saveArrayNifti(img_filter_cATP,output_filter_path_cATP, header)

        copy_files(output_original_path_PCr,output_realign_path_PCr)
        copy_files(output_original_path_cATP,output_realign_path_cATP)
    
        print("--Realing images...")
        coreg_imgs(resliced_31P_into_MNI_1H, output_filter_path_cATP, output_realign_path_PCr,output_realign_path_cATP, 'catp_anat31Pr')
        coreg_imgs(resliced_31P_into_MNI_1H, output_filter_path_cATP, output_realign_path_PCr,output_realign_path_cATP, 'anat31Pr')

    else:
        print("-Skipped Aligned 31P to 31P-1H-MNI.")

    if (args.warpMNI == 1):
        print("-Finding warp transformation anat -> MNI")
        print("--FNIRT")
        normalize_out = normalize(resliced_1H_MNI, INITIALIZATION['template']['mni'])

    else:
        print("-Skipped warp transformation anat -> MNI")
   
    if (args.invwarpMNI == 1):
        print("-Finding inversewarp transformation anat -> MNI")
        print("--Invwarp")
        normalize_out = normalize(resliced_1H_MNI, INITIALIZATION['template']['mni'])

    else:
        print("-Skipped warp transformation anat -> MNI")
   

    if (args.createROI == 1):
        print("-Create individual ROI")
        print("--Create ROI in MNI")
        mask = aggregate_mask(roi,  INITIALIZATION['atlas']['path_cor'], mask_volunteer)
        labels = get_labels(INITIALIZATION['atlas'],'labels_cor-xml')
        print("-- This ROI contains")
        print(labels.loc[roi]['#text'])
        print("--Apply individual inverse transformation to MNI")
        apply_warp(mask_volunteer, INITIALIZATION['template']['mni'], warp_file)
        apply_warp(resliced_1H_MNI, INITIALIZATION['template']['mni'], warp_file)

    else:
        print("-Skipped create ROI MNI.")
    
    if (args.computeStatistics == 1):
        print("-Compute mean in ROI")
        r_final_realign_path_cATP = add_prefix(output_realign_path_cATP, 'catp_anat31Pr')
        r_final_realign_path_PCr = add_prefix(output_realign_path_PCr, 'catp_anat31Pr')
        
        vols_cATP = openArrayImages(r_final_realign_path_cATP)
        vols_PCr = openArrayImages(r_final_realign_path_PCr)
        mask_volunteer = openArrayImages(mask_volunteer.replace('.nii', '_unwarp.nii'))
        FA = sub_par['FA']
        FA = np.asarray(FA)

        stats_pcr =  []
        stats_catp =  []
        for i in range(img_cATP.shape[0]):
            stats_pcr.append(statisticsImage(vols_PCr[i,:,:,:], mask_volunteer))
            stats_catp.append(statisticsImage(vols_cATP[i,:,:,:], mask_volunteer))
          
        plotStatMT(FA, stats_pcr, 'PCr', 'cATP', sub_par['output_dir'])
        plotStatMT(FA, stats_catp, 'cATP', 'cATP', sub_par['output_dir'])

    else:
        print("-Skipped compute Statistics")


    print("--Sucess--")


