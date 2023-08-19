import os 
import numpy as np
import matplotlib.pyplot as plt
import h5py
#Get currend directory
cwd = os.getcwd()
cwd=os.path.join(cwd,'data_19_05')
Image_dir=os.path.join(cwd,'Images')
W=[0.1,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0]
Tau=[0.1,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5]
Z=np.zeros((len(W),len(Tau)))
for i,w in enumerate(W):
    for j,tau in enumerate(Tau):
        filename=f'anderson:W={w},t={tau},n=500.h5'
        #Load data
        filename=os.path.join(cwd,filename)
        with h5py.File(filename,'r') as f:
            y=f['detection_time'][:]
        y=np.mean(y,axis=0)
        #Find the survival probability
        y=1-np.sum(y)
        #Find the survival probability at n=500
        Z[i,j]=np.log(y)
#Plot a heatmap
plt.imshow(Z,extent=[Tau[0],Tau[-1],W[0],W[-1]],aspect='auto')
plt.colorbar()
plt.xlabel(r'$\tau$')
plt.ylabel(r'$W$')
plt.title(r'Survival probability')
#Save the file
filename=f'anderson:survival_probability.png'
filename=os.path.join(Image_dir,filename)
plt.savefig(filename)

