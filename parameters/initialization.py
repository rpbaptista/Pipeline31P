# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""

import numpy as np


INITIALIZATION = dict()

INITIALIZATION['paths'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-08-28/' ,
    'anat_1H' : 'fl200200/1_012_mprage_sag_T1_160sl_iPAT2_20200819/fl200200_20200819_001_012_mprage_sag_T1_160sl_iPAT2.nii',
    'anat_31P' : 'fl200200/1_002_t1_mpr_tra_iso2_0mm_20200828/fl200200_20200828_001_002_t1_mpr_tra_iso2_0mm.nii',
    '31P_PCr' :  ['meas_MID294_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID4938_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID296_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID4940_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID297_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID4941_filter_hamming2_freq_0_echo_0.nii',
                     'meas_MID295_31P_MT_cATP_FA360_PCr_TPI_P3600_RES12_TR250_TE5_FID4939_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' : ['meas_MID294_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID4938_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID296_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID4940_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID297_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID4941_filter_hamming2_freq_-300_echo_0.nii',
                     'meas_MID295_31P_MT_cATP_FA360_PCr_TPI_P3600_RES12_TR250_TE5_FID4939_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData', 'ProcessedData'],
}



INITIALIZATION['atlas'] ={
    'path_sub' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-sub-maxprob-thr25-1mm.nii',
    'path_cor' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-cort-maxprob-thr25-1mm.nii',
    'labels_cor-xml' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-cort-maxprob-thr25-1mm.xml',
    'labels_sub-xml' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-sub-maxprob-thr25-1mm.xml',
}

INITIALIZATION['template'] = {
    'mni' : '/volatile/softwares/FSL/data/standard/MNI152_T1_2mm.nii',
}

INITIALIZATION['roi'] = {
    'cortical' : [1,2,3,4],
}

INITIALIZATION['acquisition'] = {
    'FA' : [0,10,60,360],
}
