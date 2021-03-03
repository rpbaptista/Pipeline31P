import numpy as np
import sys, os
from scipy.optimize import curve_fit
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pickle



def showPolyN(pickle_file):
    dic = pickle.load( open(pickle_file, "rb" ) )
    print(dic.shape)


pickle_file = "/neurospin/ciclops/people/Renata/ProcessedData/B1Map/31P_Volunteer/2021-01-29/fit_lin_deg_8_masked.pickle"

showPolyN(pickle_file)