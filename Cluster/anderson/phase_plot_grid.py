import os 
import numpy as np
import matplotlib.pyplot as plt
import h5py
#Get currend directory
cwd = os.getcwd()
cwd=os.path.join(cwd,'data_19_05')
Image_dir=os.path.join(cwd,'Images')
W=[0.1,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3.0]
Tau=[0.1,0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0]
K=100
x=np.arange(K,501,1)
grid=np.empty((len(W),len(Tau)))
epsilon=1.0e-3 #Tolerance
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
        mse=np.mean((y-y_fit)**2)
        if mse<epsilon:
            grid[j,i]=1
        else:
            grid[j,i]=0
        # plt.plot(x,y)
        # #Make label of the plot in scientific notation
        # plt.plot(x,alpha*x+b,label=rf'$\alpha$={alpha:.2e}')
        # plt.title(rf'Model: $W$={w},$\tau$={tau}')
        # plt.xlabel(r'$n$')
        # plt.ylabel(r'$F_n$')
        # plt.legend()
        # plt.show()
plt.imshow(grid,extent=[Tau[0],Tau[-1],W[0],W[-1]],origin='lower',aspect='auto')
plt.xticks(Tau)
plt.yticks(W)
plt.xlabel(r'$\tau$')
plt.ylabel(r'$W$')
plt.colorbar()
plt.show()
#Save the file
filename=f'grid.png'
filename=os.path.join(Image_dir,filename)
plt.savefig(filename)
plt.close()
