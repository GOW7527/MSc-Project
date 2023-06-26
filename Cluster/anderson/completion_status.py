import os 
import h5py
#get current directory
homedir = os.getcwd()
path='data_19_05'
path=os.path.join(homedir,path)
for filename in os.listdir(path):
    full_path = os.path.join(path, filename)
    with h5py.File(full_path, 'r') as f:
        print('Completion status for',filename,f['detection_time'][:].shape[0]/20000*100,'%')
