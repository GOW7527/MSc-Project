#Anderson Model
import os 
os.environ["OMP_NUM_THREADS"]="1"
import numpy as np
import h5py
import argparse
#Paths
path=os.getcwd()
path=os.path.join(path,'data_19/05')
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
        return np.abs(np.array(F))**2
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
filename=f"anderson:W={W},t={sampling_rate},n={sampling}.h5"
filepath=os.path.join(path,filename)
try: 
    with h5py.File(filepath,'r') as f:
        detection_array=f['detection_time'][:]
    N=30000-detection_array.shape[0]
except: 
    with h5py.File(filepath, 'x') as f:
        dset=f.create_dataset('detection_time',shape=(0,sampling),maxshape=(None,sampling) ,chunks=True)
    N=30000
for i in range(N):
    energy=np.random.uniform(-W/2,W/2,lattice_size)
    model=anderson(energy)
    F=model.F_n(time)
    with h5py.File(filepath,'a') as f:
        detection_time=f['detection_time']
        #Appending data
        #Resizing the dataset
        detection_time.resize((detection_time.shape[0]+1,detection_time.shape[1]))
        #Adding data
        detection_time[-1:]=F
