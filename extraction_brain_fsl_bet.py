import nibabel as nib
import numpy as np
import scipy.ndimage

path_mask_fsl = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/ignore/rcb200147_20200924_002_009_t1_mp2rage_sag_iso0_75mm_t1_mp2rage_sag_iso0_75mm_UNI-DEN_brain_mask.nii.gz'
path_mask_bet = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/ignore/outputBrainExtractionMask.nii.gz'
path_brain = '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/ignore/rcb200147_20200924_002_009_t1_mp2rage_sag_iso0_75mm_t1_mp2rage_sag_iso0_75mm_UNI-DEN.nii'
path_output =  '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/ignore/rcb200147_20200924_002_009_t1_mp2rage_sag_iso0_75mm_t1_mp2rage_sag_iso0_75mm_UNI-DEN_brain.nii.gz'
path_mask_output =  '/neurospin/ciclops/people/Renata/ProcessedData/31P_Volunteer/2020-09-24/ignore/brain_mask.nii.gz'
def add_mask(mask_1, mask_2):
    mask_1 = mask_1/np.max(mask_1)
    mask_2 = mask_2/np.max(mask_2)
    mask = mask_1 + mask_2
    mask[mask > 0] = 1
    return mask


def extract_brain_mask(mask_1, mask_2, brain):
    mask = add_mask(mask_1, mask_2)
    mask = scipy.ndimage.morphology.binary_closing(mask,np.ones((10,10,10)))
    return brain*mask, mask

nii_fsl = nib.load(path_mask_fsl)
nii_bet = nib.load(path_mask_bet)
nii_brain = nib.load(path_brain)

brain, mask = extract_brain_mask(nii_fsl.get_fdata(),nii_bet.get_fdata(),nii_brain.get_fdata())
nifti = nib.Nifti1Image(brain, None, header=nii_brain.header)
nib.save(nifti, path_output)
    
brain = extract_brain_mask(nii_fsl.get_fdata(),nii_bet.get_fdata(),nii_brain.get_fdata())
nifti = nib.Nifti1Image(mask, None, header=nii_brain.header)
nib.save(nifti, path_mask_output)
   