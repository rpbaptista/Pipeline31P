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
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-08-28/', 'ProcessedData/31P_Volunteer/2020-08-28/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-08-28/results',
    'FA' : [0,10,60,360],
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
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-09-24/', 'ProcessedData/31P_Volunteer/2020-09-24/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/results',
    'FA' : [0,10,30,60],
    'birthdate' : '1992-11-15',
    'hand' : 'L',

}

INITIALIZATION['sub02_y'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-10-09/' ,
    'anat_1H' : 'at140305_20191203_001_004_ns_mprage_pTx_V2.nii', # Vincent Gras
    'anat_31P' : 'at140305_20201009_001_002_t1_mpr_tra_iso2_0mm.nii',
    '31P_PCr' :  ['meas_MID232_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID9360_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID233_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID9361_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID236_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID9364_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID234_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID9362_filter_hamming2_freq_0_echo_0.nii',
                     'meas_MID235_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID9363_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' : ['meas_MID232_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID9360_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID233_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID9361_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID236_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID9364_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID234_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID9362_filter_hamming2_freq_-300_echo_0.nii',
                     'meas_MID235_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID9363_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-10-09/', 'ProcessedData/31P_Volunteer/2020-10-09/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-10-09/results',
    'FA' : [0,10,15,30,60],
    'birthdate' : '1992-08-12',
    'hand' : 'R',
}

INITIALIZATION['sub03_y'] = {
    'subject_dir' :  '/neurospin/ciclops/people/Renata/ReconstructedData/31P_Volunteer/2020-10-20/' ,
    'anat_1H' : 'bm190077_20201001_001_009_mprage_sag_T1_160sl.nii',
    'anat_31P' : 'bm190077_20201020_001_002_t1_mpr_tra_iso2_0mm.nii', # Caroline LeSter
    '31P_PCr' :  ['meas_MID212_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID10245_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID213_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID10246_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID216_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID10249_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID214_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID10247_filter_hamming2_freq_0_echo_0.nii',
                    'meas_MID215_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID10248_filter_hamming2_freq_0_echo_0.nii'],
    '31P_cATP' :  ['meas_MID212_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID10245_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID213_31P_MT_cATP_FA10_PCr_TPI_P3600_RES12_TR250_TE5_FID10246_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID216_31P_MT_cATP_FA15_PCr_TPI_P3600_RES12_TR250_TE5_FID10249_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID214_31P_MT_cATP_FA30_PCr_TPI_P3600_RES12_TR250_TE5_FID10247_filter_hamming2_freq_-300_echo_0.nii',
                    'meas_MID215_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID10248_filter_hamming2_freq_-300_echo_0.nii'],
    'replaceFolder' : ['ReconstructedData/31P_Volunteer/2020-10-20/', 'ProcessedData/31P_Volunteer/2020-10-20/imgs/'],
    'output_dir' : '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-10-20/results',
    'FA' : [0,10,15,30,60],
    'birthdate' : '1998-03-21',
    'hand' :'R' ,
}

INITIALIZATION['calibration'] ={
  #  'mask_path' : '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/mask_final.tif',
  #  'phantom_path' : '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/meas_MID65_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID9651_filter_hamming2_freq_0_echo_0.nii',
    'mask_path' : '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/mask_final-2.tif',
   'phantom_path' : '/neurospin/ciclops/people/Renata/ReconstructedData/Calibration_31P/meas_MID65_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID9651_filter_hamming2_freq_0_echo_0.nii',
    'true_value' : 50,
    'slice' : [12,14],
    'PCr' :  {'T1': 3.370,
              'T2': 0.1320,
              'T2e': 0.011 } , #verify
    'cATP' :  {'T1': 1.27,
             # 'T2':  02.0261,
              'T2e': 0.0065},
    'Pi' :  {'T1': 3.19,
            'T2e': 0.011} , # verify
    'Pbs' : {'T1': 6.8,
            'T2e' : 0.150}, # verify
    'TR' : 0.250,
    'FA' : 20,
    'TE' : 0.005,
    'tau' : 0.08,

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
                10,12,13,19,20,21,22,23,45,46,48],
    'cortical_in' : [
                 #(maybe not)
                24,28,29,30,31,32,36],         
}

#INITIALIZATION['acquisition'] = {
#    'FA' : [0,10,30,60],
#}
