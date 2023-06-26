import os 
import numpy as np
import matplotlib.pyplot as plt
import h5py
#Get currend directory
cwd = os.getcwd()
cwd=os.path.join(cwd,'Decay')
Image_dir=os.path.join(cwd,'Images')
W=[0.1,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,2.0,2.2,2.4,2.6,2.8,3.0]
Tau=[1.0]
K=500
x=np.arange(1,K+1,1)
for w in W:
    for tau in Tau:
        filename=f'decay:W={w},t={tau},n=500.h5'
        #Load data
        filename=os.path.join(cwd,filename)
        with h5py.File(filename,'r') as f:
            amplitude=f['amplitude'][:]
            echo=f['echo'][:]
        amplitude=amplitude[:,0:K]
        echo=echo[:,0:K]
        algebraic=amplitude/echo
        algebraic=np.mean(algebraic,axis=0)
        plt.loglog(x,algebraic)
        plt.title(rf'Model: $W$={w},$\tau$={tau}')
        plt.xlabel(r'$n$')
        # #Exponential Decay
        # exponential=np.empty(np.shape(amplitude))
        # for i in range(np.shape(echo)[0]):
        #     exponential[i]=amplitude[i]/np.geomspace(echo[i,0],echo[i,0]**K,num=K)
        # #Save the file
        # exponential=np.mean(exponential,axis=0)
        # plt.plot(x,exponential)
        filename=f'anderson:W={w},t={tau},n=500.png'
        filename=os.path.join(Image_dir,filename)
        plt.savefig(filename)
        plt.close()
