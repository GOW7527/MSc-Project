import numpy as np
import matplotlib.pyplot as plt
W=1
L=1000
c_n=[]
for i in range(0,100):
    H=np.random.uniform(low=-W/2, high=W/2, size=(L))
    c_n.append(np.sum(H)/L)
plt.plot(np.cumsum(c_n)/np.arange(1,101))
plt.show()