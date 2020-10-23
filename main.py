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
#import ants
import pandas as pd
from nipype.interfaces import spm
from nipype import config
import matplotlib.pyplot as plt

# insert at 1, 0 is the script path (or '' in REPL)
sys.path.append(os.path.join(sys.path[0],'../Utils/'))
sys.path.append(os.path.join(sys.path[0],'./libs/'))
sys.path.append(os.path.join(sys.path[0],'./parameters/'))

    
# Import homemade
#from metrics import statisticsImage
from utils import openArrayImages,createPath, openArrayImages, plotStatMT, createPathArray, createPathArray, saveArrayNifti, saveExcel, readExcel, appendExcel
from metrics import ListStatistics

#from utilsEval import generateSaveGraphIntensityFA, computeStatistics
from parameters.initialization import INITIALIZATION
from utils_own.utils import *
from metrics import statisticsImage
from utils_own.argsPipeline import argPipeline
from utils_own.quantification import getCoefficient,getCoefficient_T1_T2, meanMask, getKf,getKab,getTheoricalValues
from utils_own.model import getW1fromFAandTau
from utils_own.bloch_equations import getMagMat, mag_signal_N

# Set SPM path
#matlab_cmd = '/volatile/softwares/standalone_spm/spm12/run_spm12.sh /volatile/softwares/MATLAB/MATLAB_Compiler_Runtime/v713/ script'
#spm.SPMCommand.set_mlab_paths(matlab_cmd=matlab_cmd, use_mcr=True)
spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])

  
def run_pipeline(sub,roi_id,args):
  

    sub_par = INITIALIZATION[sub]
    calib = INITIALIZATION['calibration']
    roi = INITIALIZATION['roi'][roi_id]
      
    print("******************************** 31P MT pipeline  - v1.0************************")
    print('--------------------------'+sub+'--'+roi_id+'---------------------------------')

    # now, that I have the final mask I need to 
    print("-Load images")
    
    #Final
    anat_1H_path = createPath(sub_par['anat_1H'],sub_par['subject_dir'] )
    realign_MNI_anat_1H_path = createPath(sub_par['anat_1H'],sub_par['subject_dir'], sub_par['replaceFolder'])
    anat_31P_path = createPath(sub_par['anat_31P'],sub_par['subject_dir'] )
    realign_31P_anat_path = createPath(sub_par['anat_31P'],sub_par['subject_dir'], sub_par['replaceFolder'])

    resliced_1H_MNI = add_prefix(realign_MNI_anat_1H_path, 'fsl_r')
    resliced_1H_MNI_brain = resliced_1H_MNI.replace('.nii', '_brain.nii.gz')
    resliced_31P_into_MNI_1H = add_prefix(realign_31P_anat_path, 'r')

    warp_file = resliced_1H_MNI_brain.replace('.nii', '_warpcoef.nii')

     
    img_PCr = openArrayImages(sub_par['31P_PCr'], sub_par['subject_dir'])
    img_cATP = openArrayImages(sub_par['31P_cATP'], sub_par['subject_dir'])
  
    # Processed mask
    mask_mni = createPath( 'mask_mni'+roi_id+'.nii',sub_par['subject_dir'], sub_par['replaceFolder'])
    mask_volunteer = createPath( 'mask_volunteer'+roi_id+'.nii',sub_par['subject_dir'], sub_par['replaceFolder'])


    # Original images
    output_original_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'])
    output_original_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'])

    # Processed images
    output_filter_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'measFilter'])
    output_filter_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'measFilter'])
    output_filter_path_PCr_r = add_prefix(output_filter_path_PCr, 'r')
    output_filter_path_cATP_r = add_prefix(output_filter_path_cATP, 'r')

    output_realign_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'rmeas'])
    output_realign_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'rmeas'])
    output_realign_path_PCr_2 = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'r2meas'])
    output_realign_path_cATP_2 = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'r2meas'])

    if (args.alignAnat == 1):

        print("-Register and reslice with anatomy")
       
        print("--Realigned anat to TEMPLATE")
        calc_coreg_imgs(INITIALIZATION['template']['mni'], [anat_1H_path], os.path.join(sub_par['output_dir'],'anat_register_mni.mat'))
        apply_transf_imgs([anat_1H_path], os.path.join(sub_par['output_dir'],'inverse_anat_register_mni.mat') , [realign_MNI_anat_1H_path])
        
        print("--Reslice anat 1H into MNI")
        reslice(INITIALIZATION['template']['mni'], realign_MNI_anat_1H_path)
        aux = add_prefix(realign_MNI_anat_1H_path, 'r')
        fsl_anat(aux, resliced_1H_MNI,resliced_1H_MNI_brain, warp_file,  warp_file.replace('.nii', '_inverse.nii'), INITIALIZATION['template']['mni'])

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
        
        nii = nib.load(createPath(sub_par['31P_PCr'][0], sub_par['subject_dir']))
        header = nii.header
  
        print("--Saved filter images...")
        saveArrayNifti(img_filter_PCr,output_filter_path_PCr, header)
        saveArrayNifti(img_filter_cATP,output_filter_path_cATP, header)

        copy_files(output_original_path_PCr,output_realign_path_PCr)
        copy_files(output_original_path_cATP,output_realign_path_cATP)

        print("--Apply anat 31P to H transformation in all other 31P...")

        apply_transf_imgs(output_filter_path_PCr, os.path.join(sub_par['output_dir'],'inverse_anat1H_anat31P.mat') , output_filter_path_PCr_r, True)
        apply_transf_imgs(output_filter_path_cATP, os.path.join(sub_par['output_dir'],'inverse_anat1H_anat31P.mat') , output_filter_path_cATP_r, True)

        apply_transf_imgs(output_realign_path_PCr, os.path.join(sub_par['output_dir'],'inverse_anat1H_anat31P.mat') , output_realign_path_PCr_2, True)
        apply_transf_imgs(output_realign_path_cATP, os.path.join(sub_par['output_dir'],'inverse_anat1H_anat31P.mat') , output_realign_path_cATP_2, True)

        print("--Realing images...")
        coreg_imgs(resliced_31P_into_MNI_1H, output_filter_path_cATP_r, output_realign_path_PCr_2,output_realign_path_cATP_2, 'catp_anat31Pr')
   #     coreg_imgs(resliced_31P_into_MNI_1H, output_filter_path_cATP_r, output_realign_path_PCr,output_realign_path_cATP, 'anat31Pr')

    else:
        print("-Skipped Aligned 31P to 31P-1H-MNI.")



    if (args.createROI == 1):
        print("-Create individual ROI")
        print("--Create ROI in MNI")
        mask = aggregate_mask(roi,  INITIALIZATION['atlas']['path_cor'], mask_mni)
        labels = get_labels(INITIALIZATION['atlas'],'labels_cor-xml')
        print("-- This ROI contains")
        roi_label = roi.copy()
        roi_label[:] = [number - 1 for number in roi]

        print(labels.loc[roi_label]['#text'])
        print("--Apply individual inverse transformation to MNI")
        apply_warp(mask_mni, INITIALIZATION['template']['mni_brain'], warp_file.replace('.nii', '_inverse.nii'), out_file=mask_volunteer, forceNii=True)
        apply_warp(resliced_1H_MNI_brain, INITIALIZATION['template']['mni_brain'], warp_file, prefix='warp')
        apply_warp(add_prefix(resliced_1H_MNI_brain,'warp'), INITIALIZATION['template']['mni_brain'], warp_file, prefix='unwarp')

    else:
        print("-Skipped create ROI MNI.")
    
    if (args.computeStatistics == 1):
        print("-Compute mean in ROI")
        r_final_realign_path_cATP = add_prefix(output_realign_path_cATP_2, 'catp_anat31Pr')
        r_final_realign_path_PCr = add_prefix(output_realign_path_PCr_2, 'catp_anat31Pr')
        
        vols_cATP = openArrayImages(r_final_realign_path_cATP)
        vols_PCr = openArrayImages(r_final_realign_path_PCr)
        mask_volunteer = openArrayImages(mask_volunteer)
        FA = sub_par['FA']
        FA = np.asarray(FA)

        stats_pcr =  []
        stats_catp =  []
        for i in range(img_cATP.shape[0]):
            stats_pcr.append(statisticsImage(vols_PCr[i,:,:,:], mask_volunteer))
            stats_catp.append(statisticsImage(vols_cATP[i,:,:,:], mask_volunteer))
        
        listStatistics_cAtp = ListStatistics(stats_catp)
        listStatistics_PCr = ListStatistics(stats_pcr)
        
        print("-Save images")
        
        plotStatMT(FA, listStatistics_PCr,  'PCr', 'cATP', sub_par['output_dir'], prefix = 'b_'+sub+'_'+roi_id)
        plotStatMT(FA, listStatistics_cAtp, 'cATP', 'cATP', sub_par['output_dir'],prefix = 'b_'+sub+'_'+roi_id)
    
        print("-Save excel")
        saveExcel (FA, listStatistics_PCr, listStatistics_cAtp, 'PCr', 'cATP', sub_par['output_dir'], sufix=sub+'_'+roi_id)
    else:
        print("-Skipped compute Statistics")

    if (args.quantification == 1):
        print("-Quantification")

        print("-- Computing model")

        # Open images
        phantom = np.squeeze(openArrayImages([calib['phantom_path']]))
        mask = np.squeeze(openArrayImages([calib['mask_path']]))

        # slice
        phantom = phantom[:,:,calib['slice'][0]:calib['slice'][1]].T
       
        #Compute model
        signal_m = meanMask(phantom, mask)
        alpha_cATP = getCoefficient_T1_T2(signal = signal_m, 
                                calib = calib,
                                in_met = 'Pbs',
                                out_met= 'cATP')
        alpha_PCr = getCoefficient_T1_T2(signal = signal_m, 
                                calib = calib,
                                in_met = 'Pbs',
                                out_met= 'PCr')
        
        # read data
        listStatistics_PCr = readExcel( sub_par['output_dir'], sub+'_'+roi_id, 'PCr')
        listStatistics_cAtp = readExcel( sub_par['output_dir'], sub+'_'+roi_id, 'cATP')
    
        # Apply model
        print("-- Applying model")
        FA_sub = np.asarray(sub_par['FA'])
        concentrations = pd.concat([pd.DataFrame(sub_par['FA']), listStatistics_cAtp['mean_metabolite']/alpha_cATP, listStatistics_PCr['mean_metabolite']/alpha_PCr], axis=1)
        concentrations.columns = ['FA °','cATP concentration [mM]', 'PCr concentration [mM]']
        print(concentrations)
        appendExcel(concentrations, 'concentrations', sub_par['output_dir'], sufix=sub+'_'+roi_id)
       
        print("-- Flux")
        rangeK = np.arange(0.0,1,0.01)
        ratio = concentrations['PCr concentration [mM]'][0]/concentrations['cATP concentration [mM]'][0]
#        k, error = getKf(rangeK, list(concentrations['PCr concentration [mM]'])[-1], t, concentrations['PCr concentration [mM]'][0], calib['PCr']['T1'])
      #  Kpcr_catp = getKab(rangeK,ratio, listStatistics_PCr['mean_normalized'], FA_sub, calib, 'PCr', 'cATP')
       # print(Kpcr_catp)
        Ma, Mb = getTheoricalValues(0.30, 0.45, [0,0,1], [0,0, 0.75], FA_sub, calib, 'PCr', 'cATP')
        plt.plot(FA_sub, Ma, 'b:',label='PCr equation')
        plt.plot(FA, listStatistics_PCr['mean_normalized'],'b^'   , label='PCR real')
        plt.plot(FA_sub, Mb, 'r:', label='catp equation')
        plt.plot(FA, listStatistics_cAtp['mean_normalized'] , 'r^'   , label='catp real')
       
        plt.legend()
        plt.show()
    else:
        print("-Skipped quantification")

    print("--Sucess--")


if __name__ == '__main__':
# Treat arguments
    spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])

    parser = argparse.ArgumentParser()
    parser.add_argument("--sub",
                        help="which subject",
                        type=str,
                        default='sub01_y') 
    parser.add_argument("--roi",
                        help="which roi",
                        type=str,  
                        default='cortical_down') 
   
    parser.add_argument("--alignAnat",
                        help="1 to align mni with anats",
                        type=int,
                        default = 0) # This step is long and works really well no need to keep updating
    
    parser.add_argument("--align31P",
                        help="0/1 to align 31P images",
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
    
    parser.add_argument("--quantification",
                        help="0/1 to do four step analysis",
                        type=int,
                        default = 1)


    parser.add_argument("--BET",
                        help="0/1 to do four step analysis",
                        type=int,
                        default = 1)

    args = parser.parse_args() 
    run_pipeline(args.sub,args.roi,args)