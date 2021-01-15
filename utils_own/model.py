# author: Renata Porciuncula Baptista
# e-mail: renata.porciunculabaptista@cea.fr


import numpy as np
import math 

#def ratio(Mt):
#def getA()

def getW1fromFAandTau(FA,tau):
    """
    w1 = rapportgyroB1
    tau in sec
    FA in deg
    """
    FA_rad = np.radians(FA)
    W1 = FA_rad/tau
    return W1

def magnetization_AB(A, M0, C):
    A_inv = np.ligalg.inv(A)

    return np.exp(A*t)*[M0+ A_inv*C] - A_inv*C


def equation_Mt_simp(M0, deltaT, N, T1, TR, Kf):
    Mt = np.zeros(N)
    Mt[0] = M0
    
    for i in range(max(t.shape)-1):
        
        num = deltaT*M0/T1 + Mt[i]
        den = 1 + deltaT/T1 +deltaT*Kf
        Mt[i+1] =  num/den

    return Mt


def signal_equation(TR, M0, alpha_deg, T1):
    alpha_rad = np.radians(alpha_deg)
    num = M0*np.sin(alpha_rad)*(1-np.exp(-TR/T1))
    den = 1 - np.exp(-TR/T1)*np.cos(alpha_rad)
    return num/den

def signal_equation_T1_T2(TR, M0, alpha_deg, T1, T2, TE):
    alpha_rad = np.radians(alpha_deg)
    num = M0*np.sin(alpha_rad)*(1-np.exp(-TR/T1))*np.exp(-TE/T2)
    den = 1 - np.exp(-TR/T1)*np.cos(alpha_rad)
    return num/den

def getM0fromSignal(signal, alpha_deg, T1, TR):
    alpha_rad = np.radians(alpha_deg)
    num = 1 - np.exp(-TR/T1)*np.cos(alpha_rad)
    den = np.sin(alpha_rad)*(1-np.exp(-TR/T1))
    #print("... pondT1:", num/den)
    return signal*num/den

def getM0fromSignal_T1_T2(signal, alpha_deg, T1, TR, T2, TE):
    alpha_rad = np.radians(alpha_deg)
    num = 1 - np.exp(-TR/T1)*np.cos(alpha_rad)
    den = np.sin(alpha_rad)*(1-np.exp(-TR/T1))*np.exp(-TE/T2)
   # print("... pondT1andT2:", num/den)
    return signal*num/den

def exponential(x,a,b,c):
    return a*np.exp(-b*x) + c

