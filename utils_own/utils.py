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

def apply_transf_imgs(array_moving, output_mat_base, output_file):
    if isinstance(array_moving, str):
        apply_transf(array_moving, output_mat_base, output_file)
  
    for i in range(len(array_moving)):
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
    split = os.path.split(fullpath)
    return os.path.join(split[0], prefix + split[1])

def coreg_imgs(target_filter,source , all_files, prefix):
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

def inv_warp(warp_coef,ref):

    invwarp = fsl.InvWarp()

    invwarp.inputs.warp = warp_coef

    invwarp.inputs.reference = ref

    invwarp.inputs.output_type = "NIFTI_GZ"

    res = invwarp.run() 
    return res
def apply_warp(input_mask, ref_file, warp_file):
    aw = fsl.ApplyWarp()
    aw.inputs.in_file = input_mask
    aw.inputs.ref_file = ref_file
    aw.inputs.field_file = warp_file 
    res = aw.run()
    return res

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
    new_mask = np.in1d( data, INITIALIZATION_ROI ).reshape( atlas.shape )
    nifti = nb.Nifti1Image(new_mask,np.eye(4))
    nifti.header = hdr
    nb.save(nifti, output_filename)
    return nifti
 
def img_to_mask(image):
    return image


def computeStatisticsMT(imgs, mask, FA):
    