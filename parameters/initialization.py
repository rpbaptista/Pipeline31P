# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""

import numpy as np


INITIALIZATION = dict()

INITIALIZATION['sub01'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-08-28/' ,
    'anat_1H' : 'fl200200_20200819_001_012_mprage_sag_T1_160sl_iPAT2.nii',
    'anat_31P' : 'fl200200_20200828_001_002_t1_mpr_tra_iso2_0mm.nii',
    '31P_PCr' :  ['meas_MID294_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID4938_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID297_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID4941_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID296_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID4940_filter_hamming2_freq_0_echo_0.nii',
                     'meas_MID295_31P_MT_cATP_FA360_PCr_TPI_P3600_RES12_TR250_TE5_FID4939_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' : ['meas_MID294_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID4938_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID297_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID4941_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID296_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID4940_filter_hamming2_freq_-300_echo_0.nii',
                     'meas_MID295_31P_MT_cATP_FA360_PCr_TPI_P3600_RES12_TR250_TE5_FID4939_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-08-28/', 'ProcessedData/31P_Volunteer/2020-08-28/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/results',
    'FA' : [0,10,60,360],
}

INITIALIZATION['sub02'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-09-24/' ,
    'anat_1H' : 'cb200147_20200924_002_009_t1_mp2rage_sag_iso0_75mm_t1_mp2rage_sag_iso0_75mm_UNI-DEN.nii',
    'anat_31P' : 'cb200147_20200924_001_005_t1_mpr_tra_iso2_0mm.nii',
    '31P_PCr' :  ['meas_MID311_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID7295_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID312_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID7296_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID313_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID7297_filter_hamming2_freq_0_echo_0.nii',
                     'meas_MID314_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID7298_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' : ['meas_MID311_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID7295_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID312_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID7296_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID313_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID7297_filter_hamming2_freq_-300_echo_0.nii',
                     'meas_MID314_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID7298_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-09-24/', 'ProcessedData/31P_Volunteer/2020-09-24/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/results',
    'FA' : [0,10,30,60],

}


INITIALIZATION['atlas'] ={
    'path_sub' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-sub-maxprob-thr25-2mm.nii',
    'path_cor' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-cort-maxprob-thr25-2mm.nii',
    'labels_cor-xml' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-cort-maxprob-thr25-2mm.xml',
    'labels_sub-xml' : '/neurospin/ciclops/people/Renata/ProcessedData/Atlases/HarvardOxford-sub-maxprob-thr25-2mm.xml',
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
                10,12,13,19,20,21,22,23,45,46],
    'cortical_in' : [
                 #(maybe not)
                24,28,29,30,31,32,36],         
}

#INITIALIZATION['acquisition'] = {
#    'FA' : [0,10,30,60],
#}
