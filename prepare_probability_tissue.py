import nibabel as nib 
import numpy as np


tissues = ['/neurospin/ciclops/people/Renata/ProcessedData/Templates/avg152T1_white.nii',
'/neurospin/ciclops/people/Renata/ProcessedData/Templates/avg152T1_csf.nii',
'/neurospin/ciclops/people/Renata/ProcessedData/Templates/avg152T1_gray.nii']

nii = nib.load('/neurospin/ciclops/people/Renata/ProcessedData/Templates/MNI-prob-2mm.nii.gz')
data = nii.get_fdata()
header = nii.header

output_filename = '/neurospin/ciclops/people/Renata/ProcessedData/Templates/MNI-prob-2mm-brain.nii.gz'

data_new = np.zeros((data.shape[0], data.shape[1],data.shape[2]))

for i in range(len(tissues)):
    nii = nib.load(tissues[i])
    data = nii.get_fdata()
    print(data.shape)
    data_new = data_new + np.squeeze(data)

nifti = nib.Nifti1Image(data_new, None, header=header)
nib.save(nifti, '/neurospin/ciclops/people/Renata/ProcessedData/Templates/MNI-prob-2mm-sum.nii.gz')

print(np.unique(data_new))
data_new = data_new/np.max(data_new)
nifti = nib.Nifti1Image(data_new, None, header=header)
nib.save(nifti, output_filename)
