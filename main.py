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
from utils import openArrayImages,createPath, openArrayImages, plotStatMT, createPathArray, createPathArray, saveArrayNifti, saveExcel, readExcel, appendExcel, updateNoise
from metrics import ListStatistics, scale

#from utilsEval import generateSaveGraphIntensityFA, computeStatistics
from parameters.initialization import INITIALIZATION
from utils_own.utils import *
from metrics import statisticsImage
from utils_own.argsPipeline import argPipeline
from utils_own.quantification import getCoefficient, meanMask, getKf, getKab, getTheoricalValues, computeAlphas
from utils_own.model import getW1fromFAandTau
from utils_own.bloch_equations import getMagMat, mag_signal_N
from utils_own.b1_mapping import computeCorrectionFactor

# Set SPM path
#matlab_cmd = '/volatile/softwares/standalone_spm/spm12/run_spm12.sh /volatile/softwares/MATLAB/MATLAB_Compiler_Runtime/v713/ script'
#spm.SPMCommand.set_mlab_paths(matlab_cmd=matlab_cmd, use_mcr=True)
#
import sys

def run_pipeline(sub,roi_id,args):

    sub_par = INITIALIZATION[sub]
    calib = INITIALIZATION['calibration']
    roi = INITIALIZATION['roi'][roi_id]
    group = INITIALIZATION['group']

    print("******************************** 31P MT pipeline  - v1.0************************")
    print('--------------------------'+sub+'--'+roi_id+'---------------------------------')

    sub_par,calib = portability(sub_par,calib, group)
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
    b1_volunteer = createPath( 'b1_volunteer'+roi_id+'.nii',sub_par['subject_dir'], sub_par['replaceFolder'])


    # Original images
    output_original_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'])
    output_original_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'])

    # Processed images
    output_filter_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'measFilter'])
    output_filter_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'measFilter'])
    output_filter_path_PCr_r = add_prefix(output_filter_path_PCr, 'r')
    output_filter_path_cATP_r = add_prefix(output_filter_path_cATP, 'r')
    output_filter_path_cATP_r_2 = add_prefix(output_filter_path_cATP, '2r')

    output_realign_path_PCr = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'rmeas'])
    output_realign_path_cATP = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'rmeas'])
    output_realign_path_PCr_2 = createPathArray(sub_par['31P_PCr'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'r2meas'])
    output_realign_path_cATP_2 = createPathArray(sub_par['31P_cATP'], sub_par['subject_dir'], sub_par['replaceFolder'], ['meas', 'r2meas'])
    r_final_realign_path_cATP = add_prefix(output_realign_path_cATP_2, 'catp_anat31Pr')
    r_final_realign_path_PCr = add_prefix(output_realign_path_PCr_2, 'catp_anat31Pr')
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

        print("--Filter images: cATP images...")
        img_filter_PCr = median_filter_images(img_PCr)
        img_filter_cATP = median_filter_images(img_cATP)
        
        nii = nib.load(createPath(sub_par['31P_PCr'][0], sub_par['subject_dir']))
        header_PCr = nii.header
        nii = nib.load(createPath(sub_par['31P_cATP'][0], sub_par['subject_dir']))
        header_cATP = nii.header
  
        print("--Saved filter images...")
        saveArrayNifti(img_filter_PCr,output_filter_path_PCr, header_PCr)
        saveArrayNifti(img_filter_cATP, output_filter_path_cATP, header_cATP)
        
        print("--Align 31P with 31P using PCR (more signal)...")
        calc_coreg_imgs(output_filter_path_PCr[0], output_original_path_PCr, os.path.join(sub_par['output_dir'],'31P_31P_Pcr.mat'))
        apply_transf_imgs(output_original_path_PCr, os.path.join(sub_par['output_dir'],'inverse_31P_31P_Pcr.mat') , output_realign_path_PCr)
        apply_transf_imgs(output_original_path_cATP, os.path.join(sub_par['output_dir'],'inverse_31P_31P_Pcr.mat') , output_realign_path_cATP)
       # apply_transf_imgs(output_filter_path_cATP, os.path.join(sub_par['output_dir'],'inverse_31P_31P_Pcr.mat') , output_filter_path_cATP_r, True)
       
       
        print("--Apply anat 31P to H transformation in all other 31P...")
       # apply_transf_imgs(output_filter_path_cATP_r, os.path.join(sub_par['output_dir'],'inverse_anat1H_anat31P.mat') , output_filter_path_cATP_r_2, True)

        apply_transf_imgs(output_realign_path_PCr, os.path.join(sub_par['output_dir'],'inverse_anat1H_anat31P.mat') , output_realign_path_PCr_2, True)
        apply_transf_imgs(output_realign_path_cATP, os.path.join(sub_par['output_dir'],'inverse_anat1H_anat31P.mat') , output_realign_path_cATP_2, True)

        print("--Realing images using cATP as reference (less muscle)...")
     #   calc_coreg_imgs(resliced_31P_into_MNI_1H, [output_realign_path_cATP_2], os.path.join(sub_par['output_dir'],'test_anat.mat'))
        coreg_imgs(resliced_31P_into_MNI_1H, output_realign_path_cATP_2[0], output_realign_path_PCr_2+output_realign_path_cATP_2, 'catp_anat31Pr')

       
      #  apply_transf_imgs(output_realign_path_cATP_2, os.path.join(sub_par['output_dir'],'inverse_test_anat.mat') , r_final_realign_path_cATP,True )
      #  apply_transf_imgs(output_realign_path_PCr_2, os.path.join(sub_par['output_dir'],'inverse_test_anat.mat') , r_final_realign_path_PCr,True)

       # reslice(resliced_31P_into_MNI_1H, r_final_realign_path_cATP)
       # reslice(resliced_31P_into_MNI_1H, r_final_realign_path_PCr)
    else:
        print("-Skipped Aligned 31P to 31P-1H-MNI.")

    if (args.createROI == 1):
        print("-Create individual ROI")
        print("--Create ROI in MNI")
        if 'cortical' in roi_id:
            mask = aggregate_mask(roi,  INITIALIZATION['atlas']['path_cor'], mask_mni)
            labels = get_labels(INITIALIZATION['atlas'],'labels_cor-xml')
        else:
            mask = aggregate_mask(0.5,  roi, mask_mni)

        print("-- This ROI contains")
        if 'cortical' in roi_id:

            roi_label = roi.copy()
            roi_label[:] = [number - 1 for number in roi]
            print(labels.loc[roi_label]['#text'])
        else:
            print(roi)
        print("--Apply individual inverse transformation to MNI")
        apply_warp(mask_mni, INITIALIZATION['template']['mni_brain'], warp_file.replace('.nii', '_inverse.nii'), out_file=mask_volunteer, forceNii=True)
        apply_warp(resliced_1H_MNI_brain, INITIALIZATION['template']['mni_brain'], warp_file, prefix='warp')
        apply_warp(add_prefix(resliced_1H_MNI_brain,'warp'), INITIALIZATION['template']['mni_brain'], warp_file, prefix='unwarp')
    else:
        print("-Skipped create ROI MNI.")
    
    if (args.createIndividualB1 == 1):
        print("-Create individual B1 map")
        print("--Apply individual inverse transformation to MNI")
        b1_mni = INITIALIZATION['b1']['path']
        apply_warp(b1_mni, INITIALIZATION['template']['mni_brain'], warp_file.replace('.nii', '_inverse.nii'), out_file=b1_volunteer, forceNii=True)
        apply_warp(resliced_1H_MNI_brain, INITIALIZATION['template']['mni_brain'], warp_file, prefix='warp')
        apply_warp(add_prefix(resliced_1H_MNI_brain,'warp'), INITIALIZATION['template']['mni_brain'], warp_file, prefix='unwarp')
    else:
        print("-Skipped individual B1 MNI.")

    if (args.computeStatistics == 1):
        print("-Compute mean in ROI")
         
        vols_cATP = openArrayImages(r_final_realign_path_cATP)
        vols_PCr = openArrayImages(r_final_realign_path_PCr)
        mask_volunteer_vols = openArrayImages(mask_volunteer)
        B1_volunteer_vols = openArrayImages(b1_volunteer)

        FA = sub_par['FA']
        FA = np.asarray(FA)

        stats_pcr =  []
        stats_catp =  []

        vols_corrected_cATP = np.zeros(vols_cATP.shape)
        vols_corrected_PCr = np.zeros(vols_PCr.shape)
        
        if args.applyB1Correction == 1:
            correction_factor = computeCorrectionFactor(B1_volunteer_vols,
                                                        INITIALIZATION['b1']['FA_nominal'],
                                                        calib['TR'] ,
                                                        calib['Pbs']['T1'] )
            nib.save( nib.Nifti1Image(correction_factor, np.eye(4)), os.path.join(sub_par['output_dir'],'corrected_field.nii'))           
            for i in range(img_cATP.shape[0]):
                vols_corrected_cATP[i,:,:,:] = vols_cATP[i,:,:,:] * correction_factor
                vols_corrected_PCr[i,:,:,:]  = vols_PCr[i,:,:,:] * correction_factor
                stats_catp.append(statisticsImage(vols_corrected_cATP[i,:,:,:], mask_volunteer_vols))
                stats_pcr.append(statisticsImage(vols_corrected_PCr[i,:,:,:], mask_volunteer_vols))
        else:
            for i in range(img_cATP.shape[0]):
                stats_pcr.append(statisticsImage(vols_PCr[i,:,:,:], mask_volunteer_vols))
                stats_catp.append(statisticsImage(vols_cATP[i,:,:,:], mask_volunteer_vols))
        
            
        listStatistics_cAtp = ListStatistics(stats_catp)
        listStatistics_PCr = ListStatistics(stats_pcr)
        
        print("-Save images")
        
        plotStatMT(FA, listStatistics_PCr,  'PCr', 'cATP', sub_par['output_dir'], prefix = 'b_'+sub+'_'+roi_id)
        plotStatMT(FA, listStatistics_cAtp, 'cATP', 'cATP', sub_par['output_dir'],prefix = 'b_'+sub+'_'+roi_id)
    
        print("-Save excel")
        if args.applyB1Correction == 1:
            saveExcel (FA, listStatistics_PCr, listStatistics_cAtp, 'PCr', 'cATP', sub_par['output_dir'], sufix=sub+'_'+roi_id+'b1_corrected')

        else:
            saveExcel (FA, listStatistics_PCr, listStatistics_cAtp, 'PCr', 'cATP', sub_par['output_dir'], sufix=sub+'_'+roi_id)
    else:
        print("-Skipped compute Statistics")

    if (args.quantification == 1):
        print("-Quantification")

        print("-- Computing model")
        # Open images
        phantom = np.squeeze(openArrayImages(calib['phantom_path']))
        mask = np.squeeze(openArrayImages(calib['mask_path']))

        # slice
        noise  = np.squeeze(openArrayImages([calib['noise_acq']]))
        noise_mean = np.mean(noise)
        
        #Compute model
        alpha_PCr,alpha_cATP, reg = computeAlphas(phantom, mask, noise, calib)
        print(reg.coef_, reg.intercept_)
        # read data
        if args.applyB1Correction == 1:
            listStatistics_PCr = readExcel( sub_par['output_dir'], sub+'_'+roi_id+'b1_corrected', 'PCr')
            listStatistics_cAtp = readExcel( sub_par['output_dir'], sub+'_'+roi_id+'b1_corrected', 'cATP')
        else:
            listStatistics_PCr = readExcel( sub_par['output_dir'], sub+'_'+roi_id, 'PCr')
            listStatistics_cAtp = readExcel( sub_par['output_dir'], sub+'_'+roi_id, 'cATP')

        listStatistics_PCr = updateNoise(listStatistics_PCr, noise_mean)
        listStatistics_cAtp = updateNoise(listStatistics_cAtp, noise_mean)

        # Apply model
        print("-- Applying model")
        FA_sub = np.asarray(sub_par['FA'])
        FA_sub[1:len(sub_par['FA'])] = FA_sub[1:len(sub_par['FA'])]*calib['FA']/calib['FA_theorical'] 
        print(FA_sub)
     #   concentrations = pd.concat([pd.DataFrame(sub_par['FA']), listStatistics_cAtp['mean_metabolite']/alpha_cATP, listStatistics_PCr['mean_metabolite']/alpha_PCr], axis=1)
        concentrations = pd.concat([pd.DataFrame(sub_par['FA']), (listStatistics_cAtp['mean_metabolite']-noise_mean)/alpha_cATP, 
                                                                 (listStatistics_PCr['mean_metabolite']-noise_mean)/alpha_PCr], axis=1)
        concentrations.columns = ['FA °','cATP concentration [mM]', 'PCr concentration [mM]']
        print(concentrations)

        if args.applyB1Correction == 1:
            appendExcel(concentrations, 'concentrations', sub_par['output_dir'], sufix=sub+'_'+roi_id+'b1_corrected')
        else:
            appendExcel(concentrations, 'concentrations', sub_par['output_dir'], sufix=sub+'_'+roi_id)
       
        print("-- Kinetic constant")
        rangeK = np.arange(0.1,0.5,0.01)
        ratio = concentrations['PCr concentration [mM]'][0]/concentrations['cATP concentration [mM]'][0]
        Kpcr_catp = getKab(rangeK,ratio, listStatistics_PCr['mean_norm_wo_n'], FA_sub, calib, 'PCr', 'cATP', listStatistics_cAtp['mean_norm_wo_n'])
      #  Kpcr_catp = getKab(rangeK,ratio, listStatistics_PCr['mean_normalized'], FA_sub, calib, 'PCr', 'cATP', listStatistics_cAtp['mean_normalized'])

        print("-- is:{0} s-1 , reverse {1}".format(Kpcr_catp,ratio*Kpcr_catp))

        if args.applyB1Correction == 1:
            appendExcel(pd.DataFrame([Kpcr_catp]), 'kinetic', sub_par['output_dir'], sufix=sub+'_'+roi_id+'b1_corrected')

        else:
            appendExcel(pd.DataFrame([Kpcr_catp]), 'kinetic', sub_par['output_dir'], sufix=sub+'_'+roi_id)

        print("-- Flux")
        flux = 60*calib['density']*Kpcr_catp*concentrations['PCr concentration [mM]'][0] 

        if args.applyB1Correction == 1:
            appendExcel(pd.DataFrame([flux]), 'flux_ck', sub_par['output_dir'], sufix=sub+'_'+roi_id+'b1_corrected')
        else:
            appendExcel(pd.DataFrame([flux]), 'flux_ck', sub_par['output_dir'], sufix=sub+'_'+roi_id)

        Ma, Mb = getTheoricalValues(Kpcr_catp, Kpcr_catp*ratio, [0,0,1], [0,0, 1/ratio], FA_sub, calib, 'PCr', 'cATP')
        Ma = Ma/np.max(Ma)
        Mb = Mb/np.max(Mb)
        print(Mb)

        plt.plot(FA_sub, Ma, 'b:',label='PCr equation')
        plt.plot(FA_sub, listStatistics_PCr['mean_norm_wo_n'],'b^'   , label='PCR measured')
        plt.plot(FA_sub, Mb, 'r:', label='catp equation')
        plt.plot(FA_sub, listStatistics_cAtp['mean_norm_wo_n'] , 'r^'   , label='catp measured')
        plt.xlabel('Saturation Flip Angle °')
        plt.ylabel('Normalized signal intensity ')
        plt.title('Metabolite mean intensity in ROI '+ roi_id)
        plt.legend()
     #   plt.show()
    else:
        print("-Skipped quantification")



    print("--Success--")


def run_saveResults(sub, rois, args):
    sub_par = INITIALIZATION[sub]
    calib = INITIALIZATION['calibration']
    group = INITIALIZATION['group']
    template = INITIALIZATION['template']['mni'] 

    flux_volunteer_pcr = createPath( 'flux_volunteer_PCR.nii',sub_par['subject_dir'], sub_par['replaceFolder'])
    flux_volunteer_catp = createPath( 'flux_volunteer_cATP.nii',sub_par['subject_dir'], sub_par['replaceFolder'])

    aux = createPath( 'mask_volunteer'+rois[0] +'.nii',sub_par['subject_dir'], sub_par['replaceFolder'])
    aux_vols = np.squeeze(openArrayImages(aux))

    img = nib.load(template)
    hdr = img.header

    final_image_PCr = np.zeros(aux_vols.shape)     
    final_image_cATP = np.zeros(aux_vols.shape)     

    if (args.saveResults == 1):
        print("-saveResults")
        for roi_id in rois:
            roi = INITIALIZATION['roi'][roi_id]
            mask_volunteer = createPath( 'mask_volunteer'+roi_id+'.nii',sub_par['subject_dir'], sub_par['replaceFolder'])

            if args.applyB1Correction == 1:
                flux_PCr = readExcel( sub_par['output_dir'], sub+'_'+roi_id+'b1_corrected', 'flux_ck')
                flux_cAtp = readExcel( sub_par['output_dir'], sub+'_'+roi_id+'b1_corrected', 'flux_ck')
            else:
                flux_PCr = readExcel( sub_par['output_dir'], sub+'_'+roi_id, 'flux_ck')
                flux_cAtp = readExcel( sub_par['output_dir'], sub+'_'+roi_id, 'flux_ck')
        
            mask_volunteer_vols = np.squeeze(openArrayImages(mask_volunteer))
            mask_volunteer_vols[mask_volunteer_vols>0.5] = 1
            mask_volunteer_vols[mask_volunteer_vols<=0.5] = 0

            final_image_PCr = final_image_PCr + mask_volunteer_vols*flux_PCr[0][0]  
            final_image_cATP = final_image_cATP + mask_volunteer_vols*flux_cAtp[0][0]  

            
        nib.save( nib.Nifti1Image(final_image_PCr, None, hdr), flux_volunteer_pcr)           
        nib.save( nib.Nifti1Image(final_image_cATP, None, hdr), flux_volunteer_catp)           

    else:
        print("-Skipped saveResults")

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
       
    parser.add_argument("--createIndividualB1",
                        help="0/1 to do four step analysis",
                        type=int,
                        default = 1)
       
    parser.add_argument("--applyB1Correction",
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
    parser.add_argument("--saveResults",
                        help="0/1 to do saveResults",
                        type=int,
                        default = 1)

    parser.add_argument("--BET",
                        help="0/1 to do four step analysis",
                        type=int,
                        default = 1)

    args = parser.parse_args() 
    run_pipeline(args.sub,args.roi,args)
