import os 
os.environ["OMP_NUM_THREADS"]="1"
import numpy as np
import h5py
import argparse
#Paths
path=os.getcwd()
path=os.path.join(path,'Data')
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
        Lambda=self.Lambda*t
        w=self.w[0]
        Lambda=np.exp(1j*Lambda,dtype=np.complex_)
        u=Lambda*w@w
        return u
    def echo(self,times):
        amplitude=[]
        for t in times:
            amplitude.append(self.return_amplitude(t))
        return np.abs(np.array(amplitude,dtype=np.complex_))**2
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
#Time array 
def time_array(sampling_rate, sampling):
    arr=np.arange(sampling_rate,(sampling+1)*sampling_rate,sampling_rate)
    #Fix some size mismatch
    if arr.shape[0]>sampling:
        arr=np.arange(sampling_rate,(sampling+0.1)*sampling_rate,sampling_rate)
    return arr
#Running the script
#Parameters for first detection time 
np.random.seed(0)
parser=argparse.ArgumentParser()
parser.add_argument('--w',type=float,help='disorder strength')
parser.add_argument('--t',type=float,help='multiple of pi')
parser.add_argument('--n',type=int,help='sampling number')
args=parser.parse_args()
W=args.w
sampling_rate=args.t*np.pi
sampling=args.n
time=time_array(sampling_rate,sampling)
time_echo=np.arange(0,time[-1],0.01)
lattice_size=int(2.5*sampling)
filename=f"anderson:W={W},t={args.t},n={sampling}.h5"
filepath=os.path.join(path,filename)
try: 
    with h5py.File(filepath,'r') as f:
        energy=f['energy'][:]
    N=10000-energy.shape[0]
except: 
    with h5py.File(filepath, 'x') as f:
        dset1 = f.create_dataset('energy',shape=(0,lattice_size),maxshape=(None,lattice_size) ,chunks=True)
        dset2=f.create_dataset('detection_time',shape=(0,sampling),maxshape=(None,sampling) ,chunks=True)
        dset3=f.create_dataset('eigenvalue',shape=(0,lattice_size),maxshape=(None,lattice_size) ,chunks=True)
        dset4=f.create_dataset('eigenvector',shape=(0,lattice_size),maxshape=(None,lattice_size) ,chunks=True)
        dset5=f.create_dataset('Loschmidt Echo',shape=(0,time_echo.shape[0]),maxshape=(None,time_echo.shape[0]) ,chunks=True)
    N=10000
for i in range(N):
    energy=np.random.uniform(-W/2,W/2,lattice_size)
    model=anderson(energy)
    F=model.F_n(time)
    echo=model.echo(time_echo)
    print(i/N*100,'%')
    with h5py.File(filepath,'a') as f:
        energy_array=f['energy']
        detection_time=f['detection_time']
        eigenvalue=f['eigenvalue']
        eigenvector=f['eigenvector']
        loschmidt_echo=f['Loschmidt Echo']
        #Appending data
        #Resizing the dataset
        energy_array.resize((energy_array.shape[0]+1,energy_array.shape[1]))
        detection_time.resize((detection_time.shape[0]+1,detection_time.shape[1]))
        eigenvalue.resize((eigenvalue.shape[0]+1,eigenvalue.shape[1]))
        eigenvector.resize((eigenvector.shape[0]+1,eigenvector.shape[1]))
        loschmidt_echo.resize((loschmidt_echo.shape[0]+1,loschmidt_echo.shape[1]))
        #Adding data
        energy_array[-1:]=energy
        detection_time[-1:]=F
        eigenvalue[-1:]=model.Lambda
        eigenvector[-1:]=model.w[0]
        loschmidt_echo[-1:]=echo
    







