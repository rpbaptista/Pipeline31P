import numpy as np
import matplotlib.pyplot as plt


def phase_arrase_correction(data):
    """
     Input np array (Nc, Npts)
     It will match at the first

    """
    fft = np.fft.fft(data[0,:])
    plt.plot(fft)
    plt.show()
    phase_data = fft
    return phase_data


def get_raw_data(filename):
    # Function that reads a SIEMENS .dat file and returns a k space data
    from twixreader import Twix
    data = Twix(filename)[-1]['ima'].raw()
   # data_without_1H = np.zeros((data.shape[0],data.shape[1]-1,data.shape[2]))
    data_without_1H = data[:,1:data.shape[1],:]
    return data_without_1H

def linear_channels_comb(data):
    """
    input data (NA,NC,PTS)
    """
    Naverages = data.shape[0]
    Nchannels = data_real.shape[1]
    
    for i in range(Naverages):
        data_real = np.real(data)
        print("Combination channels", Nchannels)
        SNR = np.mean(data_real, axis=(0,2))/np.std(data_real, axis=(0,2))
    #    for i in range(Nchannels):
        print("----------SNR:", SNR)
    return np.sum(data_real, axis = 1)/Nchannels

def sum_of_squares(data):
    return np.sqrt(np.sum(np.power(data,2),axis=0))

def generalized_least_squared_channel_comb(data):
    return data

def mean_N_points(data, N=10):
    return np.mean(data[:,0:N], axis=1)