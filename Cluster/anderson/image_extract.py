import os 
import numpy as np
import matplotlib.pyplot as plt
import h5py
#Get current directory
cwd = os.getcwd()
cwd=os.path.join(cwd,'data_19_05')
Image_dir=os.path.join(cwd,'Images')
W=[0.1,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0]
Tau=[0.1,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.5]
Tau=[4.5,5.5]
x=np.arange(1,501,1)
for w in W:
    for tau in Tau:
        filename=f'anderson:W={w},t={tau},n=500.h5'
        print(filename)
        #Load data
        filename=os.path.join(cwd,filename)
        with h5py.File(filename,'r') as f:
            y=f['detection_time'][:]
        y=np.mean(y,axis=0)
        plt.plot(x,y)
        plt.yscale('log')
        plt.title(rf'Model: $W$={w},$\tau$={tau}')
        plt.xlabel(r'$n$')
        plt.ylabel(r'$F_n$')
        #Save the file
        filename=f'anderson:W={w},t={tau},n=500.png'
        filename=os.path.join(Image_dir,filename)
        plt.savefig(filename)
        plt.close()
