# plot ISMRMR2020

import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np
import os

dir_sub = 'X:\people\Renata\ProcessedData\\31P_Volunteer\\2020-09-24\imgs'
masks = []
filename_images = ['catp_anat31Prr2meas_MID311_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID7295_filter_hamming2_freq_-300_echo_0.nii',
'catp_anat31Prr2meas_MID311_31P_MT_cATP_FA0_PCr_TPI_P3600_RES12_TR250_TE5_FID7295_filter_hamming2_freq_0_echo_0.nii',
'catp_anat31Prr2meas_MID314_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID7298_filter_hamming2_freq_-300_echo_0.nii',
'catp_anat31Prr2meas_MID314_31P_MT_cATP_FA60_PCr_TPI_P3600_RES12_TR250_TE5_FID7298_filter_hamming2_freq_0_echo_0.nii']
filename_anat = 'fsl_rcb200147_20200924_002_009_t1_mp2rage_sag_iso0_75mm_t1_mp2rage_sag_iso0_75mm_UNI-DEN.nii'
niiData = nib.load(os.path.join(dir_sub, filename_anat))                
anat = niiData.get_fdata()
anat[anat>0] = 1

images = np.zeros((4,91,109,91))
for idx_img in range(len(images)):
    niiData = nib.load(os.path.join(dir_sub, filename_images[idx_img]))                
    images[idx_img,:,:,:] = niiData.get_fdata()
#f, axarr = plt.subplots(2,2,figsize=(10,30))
sliceZ = 60
plt.imshow(np.squeeze(images[0,:,:,sliceZ]).T, cmap='hot', vmin=0, vmax=150)
plt.imshow(np.squeeze(images[0,:,:,sliceZ]*anat[:,:,sliceZ]).T, cmap='YlGn', vmin=0, vmax=150)
plt.colorbar()
plt.show()