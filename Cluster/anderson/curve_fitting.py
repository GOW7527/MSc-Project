import os 
import numpy as np
import matplotlib.pyplot as plt
import h5py
#Get currend directory
cwd = os.getcwd()
cwd=os.path.join(cwd,'data_19_05')
K=100
Image_dir=os.path.join(cwd,f'algebraic_curve_fit_100')
W=[0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0]
Tau=[0.1,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.5]
x=np.log(np.arange(K,501,1))
for j,w in enumerate(W):
    for i,tau in enumerate(Tau):
        filename=f'anderson:W={w},t={tau},n=500.h5'
        #Load data
        filename=os.path.join(cwd,filename)
        with h5py.File(filename,'r') as f:
            y=f['detection_time'][:]
        y=np.log(np.mean(y[:,K-1:],axis=0))
        alpha,b=np.polyfit(x,y,1)
        y_fit=x*alpha+b
        plt.plot(x,y)
        #Make label of the plot in scientific notation
        plt.plot(x,y_fit,label=rf'$\alpha$={alpha:.2e}')
        plt.title(rf'Model: $W$={w},$\tau$={tau}')
        plt.xlabel(r'$\log(n)$')
        plt.ylabel(r'$\log (\bar{F_n})$')
        plt.legend()
        #Save the file
        filename=f'anderson:W={w},t={tau},n=500.png'
        filename=os.path.join(Image_dir,filename)
        plt.savefig(filename)
        plt.close()
