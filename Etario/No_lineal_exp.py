import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

DE = np.array([1271, 1229, 1194, 1321, 1327, 1327, 1313, 1317, 1284])
BE = np.array([123, 122, 133,  99,  84,  72,  49,  63,  91])
BE = np.array([sum(BE[:i+1]) for i in range(9)])
FE = np.array([32, 36, 56, 55, 54, 52, 25, 26, 20])

betaE_iniB = 0.15740668940826127
betaE_iniD = -0.015721087667021006

def Cuad_array(arr,t): 
    return (-arr[0] + arr[t])*(1/2) + sum(arr[:t]) 

def Fe(t,betaE):
    return FE[t]*(np.e**(t*(betaE)))

def Fez(t,betaE):
    return t*FE[t]*(np.e**(t*(betaE)))

def De(t,betaE):
    return FE[t] + (np.e**(-t*(betaE)))*(DE[0]-FE[0]-(betaE)*Cuad_array(Fe(np.arange(0,t+1,dtype=int),betaE),t))

def Be(t,betaE):    
    return BE[0] + DE[0] - FE[0] - (np.e**(-t*(betaE)))*FDe(t,betaE)

def FDe(t,betaE):
    return DE[0]-FE[0]-(betaE)*Cuad_array(Fe(np.arange(0,t+1,dtype=int),betaE),t)

def dFDe(t,betaE):
    return -Cuad_array(Fe(np.arange(0,9,dtype=int),betaE), t) -(betaE)*(Cuad_array(Fez(np.arange(0,9,dtype=int),betaE), t))

def dDe(t,betaE):
    return -t*np.e**(-t*(betaE))*FDe(t,betaE) + dFDe(t,betaE)*(np.e**(-t*(betaE)))
                                                                        
def Je(betaE):
    return np.array([-dDe(ti,betaE) for ti in range(9)])

def fD(betaE):
    R = np.array([DE[ti] - De(ti,betaE) for ti in range(9)])
    J = Je(betaE)
    
    return J.T@R

def fB(betaE):
    R = np.array([BE[ti] - Be(ti,betaE) for ti in range(9)])
    # J = -betaJ*np.array([Dj(ti, betaJ) for ti in range(9)])
    J = np.array([-dDe(ti, betaE) for ti in range(9)])
    
    return J.T@R

betaE_notLD = newton(fD,betaE_iniD)
betaE_notLB = newton(fB,betaE_iniB)

print(betaE_notLD,betaE_notLB)

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
    

graf(betaE_notLD,betaE_notLB)

def function_fit(betaJ): 
    R = np.array([DE[ti] - De(ti,betaJ) for ti in range(9)])
    return R.T@R

def graf_function_fit():
    betaJ = np.linspace(-.05,1,100)
    curva = [function_fit(betaJ_i) for betaJ_i in betaJ]
    
    plt.plot(betaJ,curva)
    plt.grid()
    
# graf_function_fit()
    