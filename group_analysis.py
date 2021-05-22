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
from utils_own.b1_mapping import imageToMNI


def run_group(group_sub,roi_id, applyB1Correction):

    concentrations_group = np.zeros((2,len(group_sub)))
    kinetic_group = np.zeros((len(group_sub)))
    flux_group = np.zeros((len(group_sub)))
    path_flux = []

    print('------------------------- GROUP RESULTS ---------------------------------')

    for i in range(len(group_sub)):    
        sub_par = INITIALIZATION[group_sub[i]]
        calib = INITIALIZATION['calibration']
        roi = INITIALIZATION['roi'][roi_id]
        group = INITIALIZATION['group']


        # Windows, linux compatiibility
        sub_par,calib = portability(sub_par,calib, group)

        realign_MNI_anat_1H_path = createPath(sub_par['anat_1H'],sub_par['subject_dir'], sub_par['replaceFolder'])
        resliced_1H_MNI = add_prefix(realign_MNI_anat_1H_path, 'fsl_r')
        resliced_1H_MNI_brain = resliced_1H_MNI.replace('.nii', '_brain.nii.gz')
        warp_file = resliced_1H_MNI_brain.replace('.nii', '_warpcoef.nii')


        flux_volunteer_pcr = createPath( 'flux_volunteer_PCR.nii',sub_par['subject_dir'], sub_par['replaceFolder'])
        quant_volunteer_catp = createPath( 'quant_volunteer_cATP.nii',sub_par['subject_dir'], sub_par['replaceFolder'])
        quant_volunteer_pcr = createPath( 'quant_volunteer_PCR.nii',sub_par['subject_dir'], sub_par['replaceFolder'])
        kinetic_volunteer = createPath( 'kin_volunteer.nii',sub_par['subject_dir'], sub_par['replaceFolder'])

        output_flux_volunteer_pcr = add_prefix(flux_volunteer_pcr, 'mni_')
        output_quant_volunteer_catp = add_prefix(quant_volunteer_catp, 'mni_')
        output_quant_volunteer_pcr = add_prefix(quant_volunteer_pcr, 'mni_')
        output_kinetic_volunteer = add_prefix(kinetic_volunteer, 'mni_')

        # read data
        if applyB1Correction == 1:
            concentrations = readExcel( sub_par['output_dir'], group_sub[i]+'_'+roi_id+'b1_corrected', 'concentrations')
            kinetic = readExcel( sub_par['output_dir'], group_sub[i]+'_'+roi_id+'b1_corrected', 'kinetic')
            flux = readExcel( sub_par['output_dir'], group_sub[i]+'_'+roi_id+'b1_corrected', 'flux_ck')
        else:
            concentrations = readExcel( sub_par['output_dir'], group_sub[i]+'_'+roi_id, 'concentrations')
            kinetic = readExcel( sub_par['output_dir'], group_sub[i]+'_'+roi_id, 'kinetic')
            flux = readExcel( sub_par['output_dir'], group_sub[i]+'_'+roi_id, 'flux_ck')
        
        
        apply_warp(flux_volunteer_pcr, 
                        INITIALIZATION['template']['mni_brain'], 
                        warp_file,
                        out_file=output_flux_volunteer_pcr,
                        forceNii=True)
        apply_warp(quant_volunteer_catp, 
                        INITIALIZATION['template']['mni_brain'], 
                        warp_file,
                        out_file=output_quant_volunteer_catp,
                        forceNii=True)
        apply_warp(quant_volunteer_pcr, 
                        INITIALIZATION['template']['mni_brain'], 
                        warp_file,
                        out_file=output_quant_volunteer_pcr,
                        forceNii=True)
        apply_warp(kinetic_volunteer, 
                        INITIALIZATION['template']['mni_brain'], 
                        warp_file,
                        out_file=output_kinetic_volunteer,
                        forceNii=True)


        if i == 0:
            flux_vol_pcr =  np.squeeze(openArrayImages(output_flux_volunteer_pcr))
            conc_vol_pcr =  np.squeeze(openArrayImages(output_quant_volunteer_pcr))
            conc_vol_catp =  np.squeeze(openArrayImages(output_quant_volunteer_catp))
            kinetic_vol =  np.squeeze(openArrayImages(output_kinetic_volunteer))
        else:
            flux_vol_pcr = flux_vol_pcr + np.squeeze(openArrayImages(output_flux_volunteer_pcr))
            conc_vol_pcr =  conc_vol_pcr+ np.squeeze(openArrayImages(output_quant_volunteer_pcr))
            conc_vol_catp = conc_vol_catp+  np.squeeze(openArrayImages(output_quant_volunteer_catp))
            kinetic_vol =  kinetic_vol +np.squeeze(openArrayImages(output_kinetic_volunteer))
            

        concentrations_group[0,i] = concentrations['PCr concentration [mM]'][0]
        concentrations_group[1,i] = concentrations['cATP concentration [mM]'][0]
        
       
        flux_group[i] = flux[0][0]
        kinetic_group[i] = kinetic[0][0]   
    flux_vol_pcr = flux_vol_pcr/len(group_sub)
    conc_vol_pcr = conc_vol_pcr/len(group_sub)
    conc_vol_catp = conc_vol_catp/len(group_sub)
    kinetic_vol = kinetic_vol/len(group_sub)

    img = nib.load(output_flux_volunteer_pcr)
    hdr = img.header
    

    nib.save( nib.Nifti1Image(flux_vol_pcr, None, hdr), os.path.join(group['output_dir'], 'average_flux.nii'))           
    nib.save( nib.Nifti1Image(conc_vol_pcr, None, hdr), os.path.join(group['output_dir'], 'average_conc_pcr.nii'))           
    nib.save( nib.Nifti1Image(conc_vol_catp, None, hdr), os.path.join(group['output_dir'], 'average_conc_catp.nii'))           
    nib.save( nib.Nifti1Image(kinetic_vol, None, hdr), os.path.join(group['output_dir'], 'average_kinectic_nii'))           

    all_list = np.asarray([concentrations_group,kinetic_group,flux_group ])
    df1 = pd.DataFrame(all_list)
    
    print("Mean PCR:{0:.2f} +-  {1:.2f}".format(np.mean(concentrations_group[0,:]),  np.std(concentrations_group[0,:])) )      
    print("Mean cATP: {0:.2f} +-  {1:.2f}".format( np.mean(concentrations_group[1,:]), np.std(concentrations_group[1,:])) ) 
    print("Kinectic constants: {0:.2f} +-  {1:.2f}".format( np.mean(kinetic_group[:]), np.std(kinetic_group[:])) ) 
    print("Flux : {0:.2f} +-  {1:.2f}".format( np.mean(flux_group[:]), np.std(flux_group[:])) ) 
    path = os.path.join(group['output_dir'], 'group_analysis_'+roi_id+'_.xlsx')
    writer = pd.ExcelWriter(path)
    df1.to_excel(writer, sheet_name='group', na_rep='')
    writer.save()
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--sub",
                        help="which subject",
                        type=str,
                        default='sub01_y') 
    parser.add_argument("--roi",
                        help="which roi",
                        type=str,  
                        default='cortical_down') 
    
    args = parser.parse_args() 
    run_group(args.sub,args.roi,args)