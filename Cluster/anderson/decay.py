#Anderson Model
import os 
os.environ["OMP_NUM_THREADS"]="1"
import numpy as np
import h5py
import argparse
#Paths
path=os.getcwd()
path=os.path.join(path,'Decay')
#Model
class anderson():
    def __init__(self,energy):
        self.energy=energy
        self.lattice_size=len(energy)
        self.H=self.hamiltonian(energy)
        self.Lambda,self.w=np.linalg.eigh(self.H)
    def hamiltonian(self,energy):
        I=np.ones(self.lattice_size-1)
        H=np.diagflat(I,1)+np.diagflat(I,-1)+np.diagflat(energy)
        H[self.lattice_size-1,0]=1
        H[0,self.lattice_size-1]=1
        return H
    def return_amplitude(self,t):
        eigenvalue_array=np.exp(-1j*self.Lambda*t,dtype=np.complex_)
        eigenstate_array=np.abs(self.w[0])**2
        u=eigenvalue_array@eigenstate_array
        return u
    def phi(self,amplitude):
        n=len(amplitude)
        phi=np.zeros(n,dtype=np.complex_)
        phi[0]=amplitude[0]
        for i in range(1,n):
            inverse=amplitude[:i][::-1]
            phi[i]=amplitude[i]-phi[:i]@inverse
        return phi
    def F_n(self,time_array):
        amplitude=[]
        for t in time_array:
            amplitude.append(self.return_amplitude(t))
        F=self.phi(amplitude)
        return np.array(F,dtype=np.complex_), np.array(amplitude,dtype=np.complex_)
#Running the script
#Parameters for first detection time 
np.random.seed(0)
parser=argparse.ArgumentParser()
parser.add_argument('--w',type=float,help='disorder strength')
parser.add_argument('--t',type=float,help='sampling rate')
parser.add_argument('--n',type=int,help='sampling number')
args=parser.parse_args()
W=args.w
sampling_rate=args.t
sampling=args.n
#Time array
time=np.zeros(sampling)
elements=sampling_rate
for i in range(sampling):
    time[i]=elements
    elements+=sampling_rate
####
lattice_size=int(2.5*sampling*sampling_rate)
filename=f"decay:W={W},t={sampling_rate},n={sampling}.h5"
filepath=os.path.join(path,filename)
try: 
    with h5py.File(filepath,'r') as f:
        detection_array=f['amplitude'][:]
    N=10000-detection_array.shape[0]
except: 
    with h5py.File(filepath, 'x') as f:
        dset_amplitude=f.create_dataset('amplitude',shape=(0,sampling),maxshape=(None,sampling) ,chunks=True,dtype=np.complex_)
        dset_echo=f.create_dataset('echo',shape=(0,sampling),maxshape=(None,sampling) ,chunks=True,dtype=np.complex_)
    N=10000
for i in range(N):
    energy=np.random.uniform(-W/2,W/2,lattice_size)
    model=anderson(energy)
    phi_k,L_k=model.F_n(time)
    with h5py.File(filepath,'a') as f:
        amplitude=f['amplitude']
        echo=f['echo']
        #Appending data
        #Resizing the dataset
        amplitude.resize((amplitude.shape[0]+1,amplitude.shape[1]))
        echo.resize((echo.shape[0]+1,echo.shape[1]))
        #Adding data
        echo[-1:]=L_k.astype(np.complex_)
        amplitude[-1:]=phi_k.astype(np.complex_)


