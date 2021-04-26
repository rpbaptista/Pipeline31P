# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:33:54 2020

@author: RP258738
"""

import numpy as np
import sys, os
from scipy.optimize import curve_fit
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pickle
sys.path.append(os.path.join(sys.path[0],'./utils_own/'))
sys.path.append(os.path.join(sys.path[0],'../../Utils/'))
import nibabel as nib

from utils import openArrayImages, saveArrayNifti, interpolateImage, prepareHeaderOS, getSSIM

from utils_own.model import * 
from utils_own.utils import * 


def computeCorrectionFactor(b1_map,FA_nominal, TR, T1):
    """
        Returns correction factor to B1 
        input = FA_nominal in degrees
    """
    import time
    import scipy.ndimage as sp_image
  
    M0 = 1
    b1_map = np.squeeze(b1_map)
    mask = np.abs(b1_map)<FA_nominal*0.10
    mask = sp_image.binary_erosion(mask, structure=np.ones((1,1,1))).astype(mask.dtype)
    SI_nominal = signal_equation(TR, 1,  FA_nominal , T1)
    correction_factor_map = SI_nominal/signal_equation(TR, M0,  b1_map, T1)
    np.place(correction_factor_map, mask, 0)


    return correction_factor_map


def allNameStr(path, name='sub-'):

    start = path.find(name) + len(name)
    stop = start + 2
    # Remove charactes from index 5 to 10
    if len(path) > stop :
        path = path[0: start:] +'_all_' + path[stop + 1::]
        return path

def showPolyN(picke_file):
    with open(picke_file, "r") as input_file:
        e = pickle.load(input_file)
        print(e)

def getFilenameB1(sub,init,DENOISE):
    patch_size = init['par_postproce']['patch_size'] 
    patch_distance = init['par_postproce']['patch_distance'] 
    degres_poly = init['par_postproce']['deg_poly']
    if DENOISE == True:
        filename_output = "result_carte_b1_"+sub+"_den_patch_size_"+str(patch_size)+"_patch_distance_"+str(patch_distance)+".nii"
        filename_fit_output = "result_carte_b1_"+sub+"_den_patch_size_"+str(patch_size)+"_patch_distance_"+str(patch_distance)+"_fit_pol"+str(degres_poly)+".nii"
        error_output = "result_error_b1_"+sub+"_den_patch_size_"+str(patch_size)+"_patch_distance_"+str(patch_distance)+".nii"
    else:
        filename_output = "result_carte_b1_"+sub+".nii"
        filename_fit_output = "result_carte_b1_"+sub+"_fit_pol"+str(degres_poly)+".nii"
        error_output = "result_error_b1_"+sub+".nii"
    return filename_output,filename_fit_output, error_output

def getReceptionPaths(path_base, N_channels):
    output = []
    for curchannels in range(N_channels):
        output.append(path_base.format(curchannels+1))

    return output 

def getFilenameFilter(init,len_array):
    patch_size = init['par_postproce']['patch_size'] 
    patch_distance = init['par_postproce']['patch_distance'] 
    filter_filename =[] 
    for i in range(len_array):
        filter_filename.append("filter_nlm_patch_size_"+str(patch_size)+"_patch_distance_"+str(patch_distance)+"_img_"+str(i)+".nii")

    return filter_filename

def imageFitPolyN(image,degree, output_dir, mask = None):

    if mask is not None:
        mask = mask /np.max(mask)
        image = image*mask
        filename_out = os.path.join(output_dir, "fit_lin_deg_{0}_masked.pickle".format(degree))
    else:
        mask = np.ones(image.shape)
        filename_out = os.path.join(output_dir, "fit_lin_deg_{0}_masked.pickle".format(degree))

    import pickle


    maks_flat = mask.reshape(-1,1)
    ind_zeros = np.argwhere(maks_flat == 0)
    ind_nonzeros = np.argwhere(maks_flat != 0)

    shape_ = image.shape
    imageFitted = np.zeros(shape_)
    poly = PolynomialFeatures(degree)

    x = np.linspace(0, shape_[0] - 1, shape_[0]) 
    y = np.linspace(0, shape_[1] - 1, shape_[1])
    z = np.linspace(0, shape_[2] - 1, shape_[2])

    X, Y, Z = np.meshgrid(x, y, z, copy=False)
    
    X_f = X.reshape(-1,1)
    Y_f = Y.reshape(-1,1)
    Z_f = Z.reshape(-1,1)
    
    coor = np.dstack((X_f,Y_f,Z_f))
    coor = coor.reshape(-1,3)
    coor_t = poly.fit_transform(coor)
   

    X_nz = np.delete(X_f,ind_zeros)
    Y_nz = np.delete(Y_f,ind_zeros)
    Z_nz = np.delete(Z_f,ind_zeros)
    
    # to fit 
    coor_nz = np.dstack((X_nz,Y_nz,Z_nz))
    coor_nz = coor_nz.reshape(-1,3)
    coor_nz_t = poly.fit_transform(coor_nz)
    
    clf = LinearRegression()
    image_flat = image.reshape(-1,1)
    image_flat_nz = np.delete(image_flat,ind_zeros)
    clf.fit(coor_nz_t, image_flat_nz )

    with open(filename_out, 'wb') as f:    
        pickle.dump(clf.coef_, f)
        pickle.dump(clf.intercept_, f)
    # to predict in all points 
    y_predict = clf.predict(coor_t)
    imageFitted = y_predict.reshape((shape_[0], shape_[1], shape_[2] ) )
    imageFitted = imageFitted*mask
  
    return imageFitted

def imageToMNI(init, sub, data):
    template = init['template']['mni'] 
    template_mask = init['template']['mni_mask'] 
    anat = init['anat'][sub]
    images = data[sub].copy()
    output_dir = init['output_dir'][sub]
    DENOISE = init['par_postproce']['DENOISE'] 
    os_factor = init['par_postproce']['os_factor'] 

    filename_output,filename_fit_output, error_output = getFilenameB1(sub,init,DENOISE)
    output_base = add_path(images, output_dir)
    map_fit_output = add_path(filename_fit_output, output_dir)
    output_realign = add_prefix(output_base, 'r_')
    output_os = add_prefix(output_base, 'os_')

    print("--Align 31P to 31P anat")    
    vols = openArrayImages(output_base)
    shape_aux = vols.shape
    nii = nib.load(output_base[0]) 
    header_os = prepareHeaderOS(nii.header, os_factor)
   

    SFdata = np.zeros((shape_aux[0],shape_aux[1]*os_factor, shape_aux[2]*os_factor, shape_aux[3]*os_factor))
    for i in range(shape_aux[0] ):
        SFdata[i,:,:,:]  = interpolateImage(vols[i,:,:,:] , os_factor)
    saveArrayNifti(SFdata, output_os, header_os)
    path_filter = add_prefix(output_os, 'filter_')
    
    vols = openArrayImages(output_os)
    vols_filter = median_filter_images(vols)
    saveArrayNifti(vols_filter,path_filter, header_os)


    calc_coreg_imgs(anat,[ path_filter[0]] , os.path.join(output_dir,'31P_31P_anat.mat'))
    forceNotRotationMat(os.path.join(output_dir,'31P_31P_anat0.mat'))
    

  #  output_realign_2 = add_prefix(output_base, '2r_')
    map_realign = add_prefix(map_fit_output, 'r_')
    # apply_transf_imgs(output_os, os.path.join(output_dir,'inverse_31P_31P_anat.mat') , output_realign, True)
    apply_transf_imgs(map_fit_output , os.path.join(output_dir,'inverse_31P_31P_anat0.mat') , map_realign, True)


    print("--Realigned anat to TEMPLATE")
    calc_coreg_imgs(template, [anat], os.path.join(output_dir,'anat_register_mni.mat'))
    realign_anat = add_prefix(anat, 'r')
    apply_transf_imgs([anat], os.path.join(output_dir,'inverse_anat_register_mni.mat') , [realign_anat])
    resliced_31P_MNI = add_prefix(realign_anat, 'fsl_r')
    warp_file = resliced_31P_MNI.replace('.nii', '_warpcoef.nii')
  #  fsl_anat(realign_anat, resliced_31P_MNI,0, warp_file,  warp_file.replace('.nii', '_inverse.nii'), template, brain=False)
    
    print("--Apply same linear transform to 31P maps")
    output_final = add_prefix(output_base, 'final_')
    map_final= add_prefix(map_fit_output, 'final_')

    apply_transf_imgs(output_realign, os.path.join(output_dir,'inverse_anat_register_mni.mat') , output_final, True)
    apply_transf_imgs(map_realign , os.path.join(output_dir,'inverse_anat_register_mni0.mat') , map_final , True)
    
    print("--Reslice anat 31P into MNI")
    reslice(resliced_31P_MNI, output_final)
    reslice(resliced_31P_MNI, map_final)
    output_r_final = add_prefix(output_final, 'r')
    map_r_final = add_prefix(map_final, 'r')

    print("--Apply warp 31P ...")
    apply_warp(resliced_31P_MNI, template, warp_file, prefix='warp',  forceNii = True)
    apply_warp(map_r_final, template, warp_file, prefix='warp',  forceNii = True)

    for i in range(len(output_r_final)):
        apply_warp(output_r_final[i] , template,  warp_file, prefix='warp', forceNii = True)

    map_mask_final = add_prefix(map_final, 'mask')
    vols = openArrayImages(add_prefix(map_r_final, 'warp'))
    mask_template = np.squeeze(openArrayImages([template_mask]))
    mask_template = mask_template/np.max(mask_template)
    shape_aux = vols.shape
    nii = nib.load(map_r_final)
    header = nii.header
    SFdata = np.zeros((shape_aux))
    for i in range(shape_aux[0] ):
        SFdata[i,:,:,:]  = vols[i,:,:,:]*mask_template

    saveArrayNifti(SFdata,[ map_mask_final]  , header)


    return map_r_final, map_mask_final

def T1mapFromYvalues(y_values, init):
    N_obs = len(y_values[:,0])
    results = np.zeros((N_obs,3))
    err = np.zeros((N_obs,3))

    for i in range(len(y_values[:,0])):
        x_values =[init['TR']]+init['TI_nominal']
        try:
          #  xdata =np.vstack((x_values,x_values)) 
          #  y_data = y_values[i,:]/np.max(y_values[i,:]) 
            pop, pcov = curve_fit(function_T1_double,
                                    x_values,
                                    y_values[i,:] ,absolute_sigma=True )
        #    print("parameters, pcov", pop, pcov)
        except RuntimeError:
            results[i,:] = -1  
            err[i,:] = -1 
            pass
    #   print(y_values[i,:],results[i])
        results[i,:]= pop #
        err[i,:]  = np.sqrt(np.diag(pcov))
    return results, err
  
def B1mapFromYvalues(y_values,init):
    results = np.zeros(y_values[:,0].shape)
    err = np.zeros(y_values[:,0].shape)

    for i in range(len(y_values[:,0])):
        x_values =[ init['T1'] ,init['TR']]
        for k in range(len(y_values[i,:])):
            x_values.append(y_values[i,k] )
        try:
            pop, pcov = curve_fit(function_B1_double,
                                    x_values,
                                    y_values[i,:] ,absolute_sigma=True )
        #    print("parameters, pcov", pop, pcov)
        except RuntimeError:
            results[i] = -1  
            err[i] = -1 
            pass
     #   print(y_values[i,:],results[i])
        results[i]= pop #
        err[i]  = np.sqrt(np.diag(pcov))
    return results, err

def yFromSFdata(SFdata):
   #TODO: GENERALIZE THIS FUNCTION 
    if len(SFdata.shape)==4:
        y_values_alpha_1 = SFdata[0,:,:,:].reshape((-1,1))
        y_values_alpha_2 = SFdata[1,:,:,:].reshape((-1,1))
        y_values_alpha_3 = SFdata[2,:,:,:].reshape((-1,1))
        y_values_alpha_4 = SFdata[3,:,:,:].reshape((-1,1))
        output = np.hstack((y_values_alpha_1 ,y_values_alpha_2,y_values_alpha_3,y_values_alpha_4))
    #    output = np.hstack((y_values_alpha_1 ,y_values_alpha_2,y_values_alpha_3))
    else:
        y_values_alpha_1 = SFdata[0,:,:].reshape((-1,1))
        y_values_alpha_2 = SFdata[1,:,:].reshape((-1,1))
        y_values_alpha_3 = SFdata[2,:,:].reshape((-1,1))
        y_values_alpha_4 = SFdata[3,:,:].reshape((-1,1))
        y_values_alpha_5 = SFdata[4,:,:].reshape((-1,1))
        y_values_alpha_6 = SFdata[5,:,:].reshape((-1,1))
        y_values_alpha_7 = SFdata[6,:,:].reshape((-1,1))
        output = np.hstack((y_values_alpha_1,
                            y_values_alpha_2,
                            y_values_alpha_3,
                            y_values_alpha_4,
                            y_values_alpha_5,
                            y_values_alpha_6,
                            y_values_alpha_7,
                            ))
    return output

def get_sequence_alpha(alpha, N=4):
    sequence = np.arange(0,N) + 1
    sequence = sequence*alpha
    return np.array(sequence).flatten()

def function_T1_double(x_values, T1, theta, A):
    TR = x_values[0]
    TI = x_values[1:8] 
 
    return equation_T1(T1,TR,TI,theta, A) 

def function_B1_double(x_values, alpha):
    T1 = x_values[0]
    TR = x_values[1]
    y_obs =[]
    for i in range(len(x_values )-2):
        y_obs.append(x_values[i+2] ) 
    N = len(x_values )-2
    alphas = get_sequence_alpha(alpha, N)
    ans = equation_B1(T1, TR, alphas, 1)
    den = np.sum(np.power(ans,2))
    num = np.sum(y_obs*ans)
    S0 = num/den
    return ans*S0

def function_B1(x_values, S0, alpha):
    T1 = x_values[0]
    TR = x_values[1]
    ans = equation_B1(T1, TR, alpha,  S0)
    
    return ans

def equation_T1(T_one, TR, T_inv, theta, S0=1):
    cos_theta = np.cos(theta)
    S_T1 = 1-(1-cos_theta)*np.exp(-T_inv/T_one)
    S_T1 = 1-(2)*np.exp(-T_inv/T_one)
    return S_T1

def equation_B1(T1, TR, alpha_1, S0=1):
    """
    DAM method no relaxed T1
    alpha_1 deg
    alpha_2 deg
    """
    S1 = signal_equation(TR, S0, alpha_1, T1)    
    return S1

def ratio_equation_b1(T1, TR, alpha_1, alpha_2, S0=1):
    """
    DAM method no relaxed T1
    alpha_1 deg
    alpha_2 deg
    """
    S1 = signal_equation(TR, S0, alpha_1, T1)
    S2 = signal_equation(TR, S0, alpha_2, T1)
    
    return S1/S2

def search_keys_sub(dict_b1_database):
    result = []

    for key in dict_b1_database:
        if key.startswith('sub-'):
            result.append(key)   
    return result

def ratio_image(SFData):
    return np.squeeze(SFData[0,:,:,:]/SFData[1,:,:,:])