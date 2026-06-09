import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

DE = np.array([1271, 1229, 1194, 1321, 1327, 1327, 1313, 1317, 1284])
BE = np.array([123, 122, 133,  99,  84,  72,  49,  63,  91])
BE = np.array([sum(BE[:i+1]) for i in range(9)])
FE = np.array([ 74, 126, 183, 248, 312, 348, 326, 333, 351])

def Cuad_array(arr,t): 
    return (-arr[0] + arr[t])*(1/2) + sum(arr[:t]) 

Int_DE = np.array([Cuad_array(DE, t) for t in range(9)])
RBE = BE - BE[0]
RFE = FE - FE[0]
RDE = DE - DE[0]

betaE_iniB = (Int_DE.T@RBE)/(Int_DE.T@Int_DE)
betaE_iniD = (Int_DE.T@(RFE-RDE))/(Int_DE.T@Int_DE)

print(betaE_iniB,betaE_iniD)

def Fe(t,beta):
    return FE[t]*(np.e**(t*(beta)))

def De(t,beta):
    return FE[t] + (np.e**(-t*(beta)))*(DE[0]-FE[0]-(beta)*Cuad_array(Fe(np.arange(0,t+1,dtype=int),beta),t))

def FDe(t,betaE):
    return DE[0]-FE[0]-(betaE)*Cuad_array(Fe(np.arange(0,t+1,dtype=int),betaE),t)

def Be(t,betaE):    
    return BE[0] + DE[0] - FE[0] - (np.e**(-t*(betaE)))*FDe(t,betaE)
    
def graf(betaB,betaD):
    fig = plt.figure(figsize=(13, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    De_curva = [De(ti,betaB) for ti in range(9)]
    Be_curva = [Be(ti,betaD) for ti in range(9)]
    
    ax1.plot(range(9),De_curva,label='De función')
    ax1.scatter(range(9),DE,label='De datos')
    
    ax2.plot(range(9),Be_curva,label='Be función')
    ax2.scatter(range(9),BE,label='Be datos')
    
    ax1.set_xticks(range(9),range(2014,2023))
    ax2.set_xticks(range(9),range(2014,2023))
    ax1.set_title('Docentes')
    ax2.set_title('Bajas')
    ax1.grid() 
    ax2.grid()
    

graf(betaE_iniD,betaE_iniB)


