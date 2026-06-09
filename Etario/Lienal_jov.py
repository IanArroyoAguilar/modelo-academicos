import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

DJ = np.array([641, 617, 650, 675, 772, 827, 797, 805, 633])
BJ = np.array([103, 101, 131, 115,  74, 122, 109, 129, 132])
BJ = np.array([sum(BJ[:i+1]) for i in range(9)])
print(BJ)
FJ = np.array([153, 175, 142, 159, 178, 198, 191, 176, 220])

def Cuad_array(arr,t): 
    return (-arr[0] + arr[t])*(1/2) + sum(arr[:t]) 

Int_DJ = np.array([Cuad_array(DJ, t) for t in range(9)])
RBJ = BJ - BJ[0]
RFJ = FJ - FJ[0]
RDJ = DJ - DJ[0]

betaJ_iniB = (Int_DJ.T@RBJ)/(Int_DJ.T@Int_DJ)
betaJ_iniD = (Int_DJ.T@(RFJ-RDJ))/(Int_DJ.T@Int_DJ)

print(betaJ_iniD,betaJ_iniB)

def Fe(t,beta):
    return FJ[t]*(np.e**(t*(beta)))

def Dj(t,beta):
    return FJ[t] + (np.e**(-t*(beta)))*(DJ[0]-FJ[0]-(beta)*Cuad_array(Fe(np.arange(0,t+1,dtype=int),beta),t))

def Bj(t,betaJ):    
    return BJ[0] + DJ[0] - FJ[0] - (np.e**(-t*(betaJ)))*FDj(t,betaJ)

def FDj(t,betaJ):
    return DJ[0]-FJ[0]-(betaJ)*Cuad_array(Fe(np.arange(0,t+1,dtype=int),betaJ),t)
    
def graf(betaB,betaD):
    fig = plt.figure(figsize=(13, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    Dj_curva = [Dj(ti,betaB) for ti in range(9)]
    Bj_curva = [Bj(ti,betaD) for ti in range(9)]
    
    ax1.plot(range(9),Dj_curva,label='Dj función')
    ax1.scatter(range(9),DJ,label='Dj datos')
    
    ax2.plot(range(9),Bj_curva,label='Bj función')
    ax2.scatter(range(9),BJ,label='Bj datos')
    
    ax1.set_xticks(range(9),range(2014,2023))
    ax2.set_xticks(range(9),range(2014,2023))
    ax1.set_title('Docentes')
    ax2.set_title('Bajas')
    ax1.grid() 
    ax2.grid()
    

graf(betaJ_iniD,betaJ_iniB)


