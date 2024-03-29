# -*- coding: utf-8 -*-
#
# pipeline 31P -
# Place License here!!
# Author: Renata Porciuncula Baptista

import xmltodict
import nibabel as nb
import pandas as pd
import numpy as np
from  scipy import ndimage
from nipype.interfaces import spm
import os
import nipype.interfaces.spm.utils as spmu
import nipype.interfaces.fsl as fsl
#def create_mask (atlas, roi):
import shutil
import gzip
from nipype.interfaces.ants.segmentation import BrainExtraction
import sys
import numbers


def portability(sub_par,calib,group):
    is_windows = hasattr(sys, 'getwindowsversion')

    if is_windows:
        sub_par['subject_dir']  = sub_par['subject_dir'].replace('/neurospin/ciclops/', 'X:/')
        sub_par['output_dir']  = sub_par['output_dir'].replace('/neurospin/ciclops/', 'X:/')
        calib['mask_path'] = calib['mask_path'].replace('/neurospin/ciclops/', 'X:/')
        calib['phantom_path'] = calib['phantom_path'].replace('/neurospin/ciclops/', 'X:/')
        calib['output_dir'] = calib['output_dir'].replace('/neurospin/ciclops/', 'X:/')
      #  print("",  sub_par['subject_dir'],  sub_par['output_dir'])
    else:
        spm.SPMCommand.set_mlab_paths(paths=os.environ['SPM_PATH'])
    return sub_par, calib
def extract_brain(anat,template, probability):
    brainextraction = BrainExtraction()
    brainextraction.inputs.dimension = 3
    brainextraction.inputs.anatomical_image =anat
    brainextraction.inputs.brain_template =template
    brainextraction.inputs.brain_probability_mask = probability
    brainextraction.run()

def realign_imgs(in_files):
    realign = spm.Realign()
    realign.inputs.in_files = in_files 
    realign.inputs.register_to_mean = False 
    realign.run()

def calc_coreg_img(target, moving, output_mat):
    coreg = spmu.CalcCoregAffine()
    coreg.inputs.target = target
    coreg.inputs.moving = moving
    coreg.inputs.mat = output_mat
    coreg.run() 

def calc_coreg_imgs(target, array_moving, output_mat_base):
    if isinstance(array_moving, str):
        calc_coreg_img(target, array_moving, output_mat_base)
      
    for i in range(len(array_moving)):
        output_mat = output_mat_base.replace('.mat', '{0}.mat'.format(i))
        calc_coreg_img(target, array_moving[i], output_mat)

def apply_transf(moving, mat_file, output_file):
    applymat = spmu.ApplyTransform()
    applymat.inputs.in_file = moving
    applymat.inputs.mat = mat_file
    applymat.inputs.out_file = output_file
    applymat.run() 

def apply_transf_imgs(array_moving, output_mat_base, output_file, same_mat= False):
    if isinstance(array_moving, str):
        apply_transf(array_moving, output_mat_base, output_file)
  
    for i in range(len(array_moving)):
        if same_mat == True:
            output_mat = output_mat_base.replace('.mat', '0.mat')
        else:
            output_mat = output_mat_base.replace('.mat', '{0}.mat'.format(i))
        
        apply_transf(array_moving[i], output_mat, output_file[i])

def reslice(target, in_files):
    r2ref = spmu.Reslice()
    if isinstance(in_files, str):
        r2ref.inputs.in_file = in_files
        r2ref.inputs.space_defining = target
        #r2ref.inputs.write_which = [1, 0]
        r2ref.run()
    else:
        for i in range(len(in_files)):
            r2ref.inputs.in_file = in_files[i]
            r2ref.inputs.space_defining = target
            #r2ref.inputs.write_which = [1, 0]
            r2ref.run()

def add_prefix(fullpath, prefix=''):
    if isinstance(fullpath, list):
        for i in range(len(fullpath)):
            split = os.path.split(fullpath[i])
            fullpath[i] = os.path.join(split[0], prefix + split[1])
    else:
        split = os.path.split(fullpath)
        fullpath = os.path.join(split[0], prefix + split[1])

    return fullpath 


#def add_sufix(fullpath, sufix=''):
#    if isinstance(fullpath, list):
#        for i in range(len(fullpath)):
#            split = os.path.split(fullpath[i])
#            fullpath[i] = os.path.join(split[0], split[1]+sufix)
#    else:
#        split = os.path.split(fullpath)
#        fullpath = os.path.join(split[0], split[1]+sufix)
#
#    return fullpath 
def fsl_mask(image, mask, outfile):
    masking = fsl.maths.ApplyMask()
    masking.inputs.in_file= image
    masking.inputs.mask_file = mask
    masking.inputs.out_file = outfile
    masking.inputs.output_type= "NIFTI"
    
    masking.run()
    
def fsl_anat(anat, T1_MNI_aligned_to_mni,brain_MNI_aligned_to_mni, path_field, inv_field, ref, brain=True):
    currentDirectory = os.getcwd()

    split = os.path.split(T1_MNI_aligned_to_mni)
    os.chdir(split[0])

    cmd = "fsl_anat -i " + anat+" --noseg --nocrop --nocleanup --nosubcortseg --nosearch --noreorient --clobber -o " + os.path.join(split[0], "aux")
    os.system(cmd)
    shutil.copy(os.path.join(split[0], "aux.anat","T1_to_MNI_nonlin_coeff.nii.gz"), path_field)
    shutil.copy(os.path.join(split[0], "aux.anat","MNI_to_T1_nonlin_field.nii.gz"), inv_field)

    with gzip.open(os.path.join(split[0], "aux.anat","T1_biascorr.nii.gz"), 'rb') as f_in:
        with open(os.path.join(split[0], "aux.anat","T1_biascorr.nii"), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    shutil.copy(os.path.join(split[0], "aux.anat","T1_biascorr.nii"), T1_MNI_aligned_to_mni)
    
    if brain == True:
        with gzip.open(os.path.join(split[0], "aux.anat","T1_biascorr_brain.nii.gz"), 'rb') as f_in:
            with open(os.path.join(split[0], "aux.anat","T1_biascorr_brain.nii"), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        shutil.copy(os.path.join(split[0], "aux.anat","T1_biascorr_brain.nii"), brain_MNI_aligned_to_mni)

    os.chdir(currentDirectory)

    #os.system("rm -rf ")
def bias_correction(anat):
    fastr = fsl.FAST()
    fastr.inputs.in_files = example_data(anat)
    fastr.inputs.output_biascorrected(add_prefix(anat,'m'))
    out = fastr.run() 

def coreg_imgs(target_filter, source, all_files, prefix):
   # for i in range(len(all_files1)):
    coreg = spm.Coregister()
    coreg.inputs.source = source
    coreg.inputs.target = target_filter
    coreg.inputs.apply_to_files = all_files
    coreg.inputs.out_prefix = prefix
    coreg.run() 

def normalize(anat, ref):
   #  norm12 = spm.Normalize12()
   # norm12.inputs.image_to_align = anat
   # if others != None:
   #     norm12.inputs.apply_to_files = others
   # return norm12.run() 
    fnt = fsl.FNIRT()
    res = fnt.run(ref_file=ref, in_file=anat) 
    return res

def copy_files(array_path_origin, array_path_dest):
    for i in range(len(array_path_origin)):
        shutil.copy(array_path_origin[i], array_path_dest[i])

def inv_warp(warp_coef,ref):

    invwarp = fsl.InvWarp()

    invwarp.inputs.warp = warp_coef

    invwarp.inputs.reference = ref

    invwarp.inputs.output_type = "NIFTI_GZ"
    invwarp.inputs.inverse_warp = warp_coef.replace('.nii', '_inverse.nii')
    res = invwarp.run() 
    return res

def apply_warp(input_mask, ref_file, warp_file, prefix=None, out_file=None, forceNii=False):
    aw = fsl.ApplyWarp()
    aw.inputs.in_file = input_mask
    aw.inputs.ref_file = ref_file
    aw.inputs.field_file = warp_file
    if prefix == None and out_file == None: 
        aw.inputs.out_file = add_prefix(input_mask, prefix='warp')
    elif out_file != None:
        aw.inputs.out_file = out_file
    else: 
        aw.inputs.out_file = add_prefix(input_mask, prefix=prefix)
    aw.inputs.output_type = "NIFTI_GZ"
    if forceNii == True:
        aw.inputs.output_type = "NIFTI"

    res = aw.run()
    return res

def BET(image_path, th=None):
    btr = fsl.BET()
    btr.inputs.in_file = image_path
    if th==None:
        btr.inputs.frac = 0.7
    else:
        btr.inputs.frac = th
    btr.inputs.output_type='NIFTI_GZ'
    btr.inputs.out_file = image_path.replace('.nii', '_brain.nii.gz')
    res = btr.run() 

def find_realign_matrix(directory):
        
    count = 0
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            count = count + 1
            data = pd.read_fwf(os.path.join(directory, file), sep=" ", header=None)
    if count != 1:
        print("Multiples file or none - error")   
        data = 0      
    return data
    
def form_translation_matrix(array_translation):
    matrix = np.eyes(np.size(array_translation)+1)
    for i in range(np.size(array_translation)):
        matrix[i,-1] = array_translation[i]
    return matrix

#def apply_translation(imgs, matrix):
#    for i in range(imgs.shape[0]):
#        matrix_translation = form_translation_matrix(matrix[i,0:2])
#        img = np.squeeze(imgs[i,:,:,:])


def median_filter_images(array_images, size=2):
    output = np.zeros(array_images.shape)
    for i in range(array_images.shape[0]):
        output[i,:,:,:] = median_filter(np.squeeze(array_images[i,:,:,:]),size)
    return output

def median_filter(image,size=2):
    return ndimage.median_filter(image, size=size)

def get_labels(INITIALIZATION_ATLAS, label_part):
    with open(INITIALIZATION_ATLAS[label_part]) as fd:
        dic = xmltodict.parse(fd.read())
        aux = dic['atlas']['data']['label']
        return pd.DataFrame(aux)
         
def aggregate_mask(INITIALIZATION_ROI,  atlas, output_filename):
    img = nb.load(atlas)
    hdr = img.header
    data = img.get_fdata()
    if isinstance(INITIALIZATION_ROI, numbers.Number):
        new_mask = data > INITIALIZATION_ROI
    else:
        new_mask = np.in1d( data, INITIALIZATION_ROI ).reshape( data.shape )
    nifti = nb.Nifti1Image(new_mask.astype(int),None, header=hdr)
    nb.save(nifti, output_filename)
    return nifti
 
def img_to_mask(image):
    return image


def computeStatisticsMT(imgs, mask, FA):
    return 0