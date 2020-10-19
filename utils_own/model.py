import numpy as np
import math 

def signal_equation(TR, M0, alpha_deg, T1):
    alpha_rad = math.radians(alpha_deg)
    num = M0*np.sin(alpha_rad)*(1-np.exp(-TR/T1))
    den = 1 - np.exp(-TR/T1)*np.cos(alpha_rad)
    return num/den

def signal_equation_T1_T2(TR, M0, alpha_deg, T1, T2, TE):
    alpha_rad = math.radians(alpha_deg)
    num = M0*np.sin(alpha_rad)*(1-np.exp(-TR/T1))*np.exp(-TE/T2)
    den = 1 - np.exp(-TR/T1)*np.cos(alpha_rad)
    return num/den

def getM0fromSignal(signal, alpha_deg, T1, TR):
    alpha_rad = math.radians(alpha_deg)
    num = 1 - np.exp(-TR/T1)*np.cos(alpha_rad)
    den = np.sin(alpha_rad)*(1-np.exp(-TR/T1))
    #print("... pondT1:", num/den)
    return signal*num/den

def getM0fromSignal_T1_T2(signal, alpha_deg, T1, TR, T2, TE):
    alpha_rad = math.radians(alpha_deg)
    num = 1 - np.exp(-TR/T1)*np.cos(alpha_rad)
    den = np.sin(alpha_rad)*(1-np.exp(-TR/T1))*np.exp(-TE/T2)
   # print("... pondT1andT2:", num/den)
    return signal*num/den

def exponential(x,a,b,c):
    return a*np.exp(-b*x) + c

