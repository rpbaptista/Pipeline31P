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

sys.path.append(os.path.join(sys.path[0],'./utils_own/'))

from utils_own.model import * 
from utils_own.utils import * 
"""
def yFromSFdata(SFdata):
    y_values_alpha_1 = SFdata[0,:,:,:].reshape((-1,1))
    y_values_alpha_2 = SFdata[1,:,:,:].reshape((-1,1))
    return np.hstack((y_values_alpha_1 ,y_values_alpha_2))
def get_sequence_alpha(alpha):
    return np.array([alpha, 2*alpha]).flatten()
"""
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

def imageToMNI(template,anat,image, output_dir):
    print("--Realigned anat to TEMPLATE")
    calc_coreg_imgs(template, [anat], os.path.join(output_dir,'anat_register_mni.mat'))
    
    realign_anat = add_prefix(anat, 'r')
    resliced_1H_MNI = add_prefix(realign_anat, 'fsl_r')
    warp_file = resliced_1H_MNI.replace('.nii', '_warpcoef.nii')

    apply_transf_imgs([anat], os.path.join(output_dir,'inverse_anat_register_mni.mat') , [realign_anat])
    
    print("--Reslice anat 1H into MNI")
    reslice(template, realign_anat)
    aux = add_prefix(realign_anat, 'r')
    fsl_anat(aux, resliced_1H_MNI,0, warp_file,  warp_file.replace('.nii', '_inverse.nii'), template, brain=False)
    return 0


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
    y_values_alpha_1 = SFdata[0,:,:,:].reshape((-1,1))
    y_values_alpha_2 = SFdata[1,:,:,:].reshape((-1,1))
    y_values_alpha_3 = SFdata[2,:,:,:].reshape((-1,1))
    y_values_alpha_4 = SFdata[3,:,:,:].reshape((-1,1))
    return np.hstack((y_values_alpha_1 ,y_values_alpha_2,y_values_alpha_3,y_values_alpha_4))
def get_sequence_alpha(alpha):
    return np.array([alpha, 2*alpha, 3*alpha, 4*alpha]).flatten()

def function_B1_double(x_values, alpha):
    T1 = x_values[0]
    TR = x_values[1]
    y_obs =[]
    for i in range(len(x_values )-2):
        y_obs.append(x_values[i+2] ) 

    alphas = get_sequence_alpha(alpha)
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

def equation_B1(T1, TR, alpha_1, S0=1):
    """
    DAM method no relaxed T1
    alpha_1 deg
    alpha_2 deg
    """
    S1 = signal_equation(TR, S0, alpha_1, T1)    
    return S1

# def ratio_equation_b1(T1, TR, alpha_1, alpha_2, S0=1):
#     """
#     DAM method no relaxed T1
#     alpha_1 deg
#     alpha_2 deg
#     """
#     S1 = signal_equation(TR, S0, alpha_1, T1)
#     S2 = signal_equation(TR, S0, alpha_2, T1)
    
    return S1/S2
def search_keys_sub(dict_b1_database):
    result = []

    for key in dict_b1_database:
        if key.startswith('sub-'):
            result.append(key)   
    return result

def ratio_image(SFData):
    return np.squeeze(SFData[0,:,:,:]/SFData[1,:,:,:])