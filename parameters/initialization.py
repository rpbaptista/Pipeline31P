# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""

import numpy as np


INITIALIZATION = dict()




INITIALIZATION['sub00_y'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-08-28/' ,
    'anat_1H' : 'fl200200_20200819_001_012_mprage_sag_T1_160sl_iPAT2.nii', # Florent M.
    'anat_31P' : 'fl200200_20200828_001_002_t1_mpr_tra_iso2_0mm.nii',
    '31P_PCr' :  ['meas_MID294_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID4938_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID297_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID4941_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID296_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID4940_filter_hamming2_freq_0_echo_0.nii',
                     'meas_MID295_31P_MT_cATP_FA360_PCr_TPI_P3600_RES12_TR250_TE5_FID4939_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' : ['meas_MID294_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID4938_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID297_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID4941_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID296_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID4940_filter_hamming2_freq_-300_echo_0.nii',
                     'meas_MID295_31P_MT_cATP_FA360_PCr_TPI_P3600_RES12_TR250_TE5_FID4939_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-08-28/', 'ProcessedData/FluxEstimation/31P_Volunteer/2020-08-28/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/FluxEstimation/31P_Volunteer/2020-08-28/results',
    'FA' : [0,20,120,720],
    'birthdate' : '2001-03-19',
    'hand' : 'R' ,
}

INITIALIZATION['sub01_y'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-09-24/' ,

    'anat_1H' : 'cb200147_20200924_002_009_t1_mp2rage_sag_iso0_75mm_t1_mp2rage_sag_iso0_75mm_UNI-DEN.nii', # Me
    'anat_31P' : 'cb200147_20200924_001_005_t1_mpr_tra_iso2_0mm.nii',
    '31P_PCr' :  ['meas_MID311_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID7295_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID312_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID7296_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID313_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID7297_filter_hamming2_freq_0_echo_0.nii',
                     'meas_MID314_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID7298_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' : ['meas_MID311_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID7295_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID312_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID7296_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID313_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID7297_filter_hamming2_freq_-300_echo_0.nii',
                     'meas_MID314_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID7298_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-09-24/', 'ProcessedData/FluxEstimation/31P_Volunteer/2020-09-24/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/FluxEstimation/31P_Volunteer/2020-09-24/results',    
    'FA' : [0,20,60,120],
    'birthdate' : '1992-11-15',
    'hand' : 'L',

}

INITIALIZATION['sub02_y'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-10-09/' ,
    'anat_1H' : 'at140305_20191203_001_004_ns_mprage_pTx_V2.nii', # Vincent Gras
    'anat_31P' : 'at140305_20201009_001_002_t1_mpr_tra_iso2_0mm.nii',
    '31P_PCr' :  ['meas_MID232_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID9360_filter_hamming2_freq_0_echo_0.nii',
  #                  'meas_MID233_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID9361_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID236_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID9364_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID234_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID9362_filter_hamming2_freq_0_echo_0.nii',
                     'meas_MID235_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID9363_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' : ['meas_MID232_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID9360_filter_hamming2_freq_-300_echo_0.nii',
  #                  'meas_MID233_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID9361_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID236_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID9364_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID234_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID9362_filter_hamming2_freq_-300_echo_0.nii',
                     'meas_MID235_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID9363_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-10-09/', 'ProcessedData/FluxEstimation/31P_Volunteer/2020-10-09/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/FluxEstimation/31P_Volunteer/2020-10-09/results',
  #  'FA' : [0,20,30,60,120],
    'FA' : [0,30,60,120],
    'birthdate' : '1992-08-12',
    'hand' : 'R',
}

INITIALIZATION['sub03_y'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-10-20/' ,
    'anat_1H' : 'bm190077_20201001_001_009_mprage_sag_T1_160sl.nii',
    'anat_31P' : 'bm190077_20201020_001_002_t1_mpr_tra_iso2_0mm.nii', # Caroline LeSter
    '31P_PCr' :  ['meas_MID212_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID10245_filter_hamming2_freq_0_echo_0.nii',
  #                  'meas_MID213_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID10246_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID216_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID10249_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID214_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID10247_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID215_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID10248_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' :  ['meas_MID212_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID10245_filter_hamming2_freq_-300_echo_0.nii',
   #                 'meas_MID213_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID10246_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID216_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID10249_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID214_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID10247_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID215_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID10248_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-10-20/', 'ProcessedData/FluxEstimation/31P_Volunteer/2020-10-20/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/FluxEstimation/31P_Volunteer/2020-10-20/results',
    # 'FA' : [0,20,30,60,120],
    'FA' : [0,30,60,120],
    'birthdate' : '1998-03-21',
    'hand' :'R' ,
}

#OLD VOLUNTEERS
INITIALIZATION['sub01_o'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-10-23/' ,
    'anat_1H' : 'fb200436_20201023_001_019_t1_mp2rage_sag_iso0_75mm_t1_mp2rage_sag_iso0_75mm_UNI-DEN.nii',# Me
    'anat_31P' : 'fb200436_20201023_001_005_t1_mpr_tra_iso2_0mm.nii', 
    '31P_PCr' :  ['meas_MID153_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID10420_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID156_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID10423_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID154_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID10421_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID155_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID10422_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' :  ['meas_MID153_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID10420_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID156_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID10423_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID154_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID10421_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID155_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID10422_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-10-23/', 'ProcessedData/FluxEstimation/31P_Volunteer/2020-10-23/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/FluxEstimation/31P_Volunteer/2020-10-23/results',
    'FA' : [0,30,60,120],
    'birthdate' : '',
    'hand' :'R' ,
}
"""
INITIALIZATION['sub02_o'] = {
   'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-10-30/' ,
    'anat_1H' : '',
    'anat_31P' : '', # Me
    '31P_PCr' :  ['',
                    '',
                    '',
                    ''],
    '31P_cATP' :  ['',
                    '',
                    '',
                    ''],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-10-30/', 'ProcessedData/FluxEstimation/31P_Volunteer/2020-10-30/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/FluxEstimation/31P_Volunteer/2020-10-30/results',
    'FA' : [0,30,60,120],
    'birthdate' : '',
    'hand' :'R' ,
}

INITIALIZATION['sub03_o'] = {
   'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-10-30/' ,
    'anat_1H' : '',
    'anat_31P' : '', # Me
    '31P_PCr' :  ['',
                    '',
                    '',
                    ''],
    '31P_cATP' :  ['',
                    '',
                    '',
                    ''],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-10-30/', 'ProcessedData/FluxEstimation/31P_Volunteer/2020-10-30/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/FluxEstimation/31P_Volunteer/2020-10-30/results',
    'FA' : [0,30,60,120],
    'birthdate' : '',
    'hand' :'R' ,
}
"""

INITIALIZATION['calibration'] ={
 #   'mask_path' : '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/Mask_new_shim_2.tif',
  #  'mask_path' : '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/Mask-new_shim.tif',
    'mask_path' :[ '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/mask_all_phantom_md103_50mM_small.nii',
    '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/mask_all_phantom_md103_50mM_small.nii'], 
    'phantom_path' :[ '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/phantom_md103_50mM.nii'
                        ,'/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/phantom_mid122_25mM.nii'
                        ] ,
    'noise_acq' : '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/voltage-zero-pcr.nii', 
    'true_value' :[
        50
       ,25 
      ] , #mM
    'slice' : [9,10],
    # T1,  T2 in vivo 31p magnetici (T1 aqui é apparent)
    # T2e measured by us
    'PCr' :  {'T1': 3.37,
              'T2': 0.1320,
              'T2e': 0.011 } , #verify

    'cATP' :  {'T1': 1.27,
              'T2':  0.0261,
              'T2e': 0.0065},

  #  'Pi' :  {'T1': 3.2,
  #          'T2e': 0.011} , # verify

    'Pbs' : {'T1': 6.7, # here is another reference that evaluate free T1 31P MRS healthy
            'T2e' : 0.011}, # verify

    'TR' : 0.250,
    'FA' : 25,
    'TE' : 0.005,
    'tau' : 0.08, # time saturation in s
    'FA_theorical' : 25,
    'density': 1.05

}

INITIALIZATION['atlas'] ={
    'path_sub' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-sub-maxprob-thr25-2mm.nii',
    'path_cor' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-cort-maxprob-thr25-2mm.nii',
    'labels_cor-xml' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-cort-maxprob-thr25-2mm.xml',
    'labels_sub-xml' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-sub-maxprob-thr25-2mm.xml',
  #  'path_white' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/avg152T1_white.nii',
  #  'path_gray' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/avg152T1_gray-1.nii'
    
}

INITIALIZATION['template'] = {
    'mni' : '/volatile/softwares/FSL/data/standard/MNI152_T1_2mm.nii',
    'mni_brain' : '/volatile/softwares/FSL/data/standard/MNI152_T1_2mm_brain.nii',
    'mni_prob' : '/neurospin/ciclops/people/Renata/ProcessedData/Templates/MNI-prob-2mm-brain.nii.gz',

}

INITIALIZATION['roi'] = {
    'cortical_up' : [1, 
                2,4,7,8,42, #(maybe not)
                5,6,9,11,41],
    'cortical_down' : [
                15,16,17,43,14, #(maybe not)
                10,12,13,19,20,21,22,23,45,46,48],
    'cortical_occ_pole'    : [48],         
    'cortical_in' : [
                 #(maybe not)
                24,28,29,30,31,32,36],
    'wm' :  '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/MNI152_T1_2mm_brain_wm.nii',
    'gm' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/MNI152_T1_2mm_brain_gm.nii'        
}

INITIALIZATION['b1'] ={
    'path' : '/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/result_carte_b1_sub-_all_fit_pol8_PA_divide_255.nii',
    'FA_nominal' : 12,
    'path_phantom' : '',
} 

INITIALIZATION['group'] ={
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/FluxEstimation/31P_Volunteer',
}  
