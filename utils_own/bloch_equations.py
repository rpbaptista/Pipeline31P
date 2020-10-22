



import numpy as np
from scipy.linalg import expm
def magnetization_signal( t, dwa, dwb, M0a, M0b, kab, kba,t_A, t_B, w1):
    
    """ Function to calculate transfer two pool based on  Bottomley et al 2002
    Input: dwa,dwb rad/s
             """

    A = np.array(
        ((-1/t_A['T2e']-kab,              dwa,                   0,       kba,         0,     0),
        (-dwa,               - 1/t_A['T2e']-kab,                   w1,       0,          kba,   0),
        (0,                             -w1,      -1/t_A['T1']-kab,       0,          0,    kba),
        (kab,                            0,                    0,   -1/t_B['T2e']-kba,         dwb,           0,),
        (0,                              kab,                  0,                  -dwb, -1/t_B['T2e']-kba,    w1),
        (0,                              0,                    kab,                0,        -w1,    -1/t_B['T1']-kba))
    )

    C = np.array((0,0,abs_vec(M0a)/t_A['T1'],0,0,abs_vec(M0b)/t_B['T1']))
    
    
    Ra = zrot(np.degrees(2*np.pi*dwa*t))
    Rb = zrot(np.degrees(2*np.pi*dwb*t))
    Rz = np.zeros((3,3))
    Rflip = np.block([[Ra,Rz],[Rz,Rz]])
    
    A_inv = np.linalg.inv(A)
    M0 = np.concatenate((M0a, M0b)) 
    
    return (expm(A*t)@(M0+A_inv@C) - A_inv@C) @Rflip

def srsignal(flip,T1,T2,TE,TR,dfreq):
    """ 	srsignal(flip,T1,T2,TE,TR,dfreq)
 
	Calculate the steady state signal at TE for repeated
	excitations given T1,T2,TR,TE .  Force the
	transverse magnetization to zero before each excitation.
	dfreq is the resonant frequency in Hz.  flip in deg. """

    Rflip = yrot(flip)
    [Atr,Btr] = freeprecess(TR-TE,T1,T2,dfreq)
    [Ate,Bte] = freeprecess(TE,T1,T2,dfreq)

    # 	Force transverse magnetization to 0 before excitation.
    Atr = np.array(((0, 0, 0),(0, 0 ,0),(0, 0, 1)))@Atr

    #  % Let 	M1 be the magnetization just before the tip.
    # %	M2 be just after the tip.
    # %	M3 be at TE.
    # %
    # % then
    # %	M2 = Rflip * M1
    # %	M3 = Ate * M2 + Bte
    # %	M1 = Atr * M3 + Btr
    # %
    # % Solve for M3...
    # %
    # %	M3 = Ate*Rflip*Atr*M3 + (Ate*Rflip*Btr+Bte)

    Mss = np.linalg.inv(np.eye(3)-Ate@Rflip@Atr) @ (Ate@Rflip@Btr+Bte)
    Msig = Mss[0]+np.imag(Mss[1])

    return Msig, Mss 



def freeprecess(T,T1,T2,df):
    """  	Function simulates free precession and decay
	over a time interval T, given relaxation times T1 and T2
	and off-resonance df.  Times in s, off-resonance in Hz. """
 
    phi = 2*np.pi*df*T	# Resonant precession, radians.
    phi_deg = np.degrees(phi)
    E1 = np.exp(-T/T1)	
    E2 = np.exp(-T/T2)

    Afp = np.dot(np.array(((E2, 0, 0),(0, E2, 0),(0, 0, E1))),zrot(phi_deg))
    Bfp = np.array((0, 0, 1-E1)).T
    return Afp, Bfp



# -----------------------------------  auxiliary functions


def abs_vec(vec):
    return np.sqrt(vec[0]*vec[0]+vec[1]*vec[1]+vec[2]*vec[2])

def tranverse_relaxation(t,T2):
    A = np.zeros((3,3))
    A[0,0] = np.exp(-t/TE)
    A[1,1] = np.exp(-t/TE)
    A[2,2] = 1
    return A

def longitudinal_relaxation(t,T1):
    A = np.zeros((3,3))
    A[0,0] = 1
    A[1,1] = 1
    A[2,2] = np.exp(-t/T1)
    B = np.zeros((3,1))
    B[3,0] = 1 - np.exp(-t/TR)
    return A,B


def zrot(phi_deg):
    phi = np.radians(phi_deg)
    Rz = np.zeros((3,3))
    Rz[0,0] =  np.cos(phi)
    Rz[0,1] =  -np.sin(phi)
    Rz[1,0] = np.sin(phi)
    Rz[1,1] = np.cos(phi)
    Rz[2,2] = 1
    return np.asarray(Rz)

def xrot(phi_deg):
    phi = np.radians(phi_deg)
    Rx = np.array(((1,0,0),(0,np.cos(phi),-np.sin(phi)),(0,np.sin(phi), np.cos(phi))))
    return Rx

def yrot(phi_deg):
    phi = np.radians(phi_deg)
    c = np.cos(phi)
    s = np.sin(phi)
    Ry = np.array(((c,0,s),(0,1,0),(-s,0, c)))
    return Ry

def throt(phi_deg, theta_deg):
    Rz = zrot(-theta_deg)
    Rx = xrot(phi_deg)
    return  np.linalg.inv(Rz)*Rx*Rz

########################


# def spgrsignal(flip,T1,T2,TE,TR,df = 0, Nex=  100,inc= 117/180*pi):
#     """ 	function [Msig,Mss]=spgrsignal(flip,T1,T2,TE,TR,df,Nex,inc)
    
#     	Function calculates the signal from an RF-spoiled sequence
#     	after Nex excitations.
    
#      """

#     Nf = 100 # Simulate 100 different gradient-spoiled spins.
#     phi = np.arange(1,Nf,1)/Nf*2*pi#
#     phi_deg = np.degrees(phi)

#     M=zeros((3,Nf,Nex+1))

        
#     [Ate,Bte] = freeprecess(TE,T1,T2,df)
#     [Atr,Btr] = freeprecess(TR-TE,T1,T2,df)

#     M = [zeros(2,Nf);ones(1,Nf)]
#     on = ones(1,Nf)
        
#     Rfph = 0
#     Rfinc = inc

#     for n in range(Nex):

#         A = Ate @ throt(flip,Rfph)
#         B = Bte
#         M = A@M+B@on

#         Msig = mean( np.squeeze(M[0,:]+i@M[1,:]) ) * np.exp(-i*Rfph)
#         Mss = M

#         M=Atr@M+Btr@on

#         for k in range(Nf):
#             M[:,k] = zrot(phi_deg[k])@M[:,k]
       
#         Rfph = Rfph+Rfinc
#         Rfinc = Rfinc+inc
    