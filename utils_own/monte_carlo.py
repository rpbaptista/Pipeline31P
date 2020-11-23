# Renata Porciuncula Baptista
# E-mail: renata.porciunculabaptista@cea.r
# 
# 
# Goal : simulate Monte Carlo results 



from scipy.stats import rice
import numpy as np
from scipy import stats as scst
import numpy as np
import matplotlib.pyplot as plt

mean_image = 125
std_image = 30
image_mean_0 = 400
mean = mean_image/image_mean_0
sigma = std_image/image_mean_0
Rsci=rice(mean,scale=sigma)
xs=np.linspace(0,25,1000)
plt.plot(xs,Rsci.pdf(xs),'r')
plt.show()
mean, var, skew, kurt = rice.stats(2, moments='mvsk')
print(mean)
r = rice.rvs(b, size=1000)