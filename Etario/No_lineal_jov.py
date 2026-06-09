import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
from scipy.optimize import curve_fit

DJ = np.array([641, 617, 650, 675, 772, 827, 797, 805, 633])
BJ = np.array([103, 101, 131, 115,  74, 122, 109, 129, 132])
BJ = np.array([sum(BJ[:i+1]) for i in range(9)])
FJ = np.array([153, 175, 142, 159, 178, 198, 191, 176, 220])

betaJ_iniB = 0.15740668940826127
betaJ_iniD = -0.015721087667021006

def Cuad_array(arr,t): 
    return (-arr[0] + arr[t])*(1/2) + sum(arr[:t]) 

def Fe(t,betaJ):
    return FJ[t]*(np.e**(t*(betaJ)))

def Fez(t,betaJ):
    return t*FJ[t]*(np.e**(t*(betaJ)))

def Dj(t,betaJ):
    return FJ[t] + (np.e**(-t*(betaJ)))*(DJ[0]-FJ[0]-(betaJ)*Cuad_array(Fe(np.arange(0,t+1,dtype=int),betaJ),t))

def Bj(t,betaJ):    
    return BJ[0] + DJ[0] - FJ[0] - (np.e**(-t*(betaJ)))*FDj(t,betaJ)

def FDj(t,betaJ):
    return DJ[0]-FJ[0]-(betaJ)*Cuad_array(Fe(np.arange(0,t+1,dtype=int),betaJ),t)

def dFDj(t,betaJ):
    return -Cuad_array(Fe(np.arange(0,9,dtype=int),betaJ), t) -(betaJ)*(Cuad_array(Fez(np.arange(0,9,dtype=int),betaJ), t))

def dDj(t,betaJ):
    return -t*np.e**(-t*(betaJ))*FDj(t,betaJ) + dFDj(t,betaJ)*(np.e**(-t*(betaJ)))
                                                                        
def Jj(betaJ):
    return np.array([-dDj(ti,betaJ) for ti in range(9)])

def fD(betaJ):
    R = np.array([DJ[ti] - Dj(ti,betaJ) for ti in range(9)])
    J = Jj(betaJ)
    
    return J.T@R

def fB(betaJ):
    R = np.array([BJ[ti] - Bj(ti,betaJ) for ti in range(9)])
    # J = -betaJ*np.array([Dj(ti, betaJ) for ti in range(9)])
    J = np.array([-dDj(ti, betaJ) for ti in range(9)])
    
    return J.T@R

def function_fit(betaJ): 
    R = np.array([DJ[ti] - Dj(ti,betaJ) for ti in range(9)])
    return R.T@R
    
    
    
betaJ_notLD = newton(fD,betaJ_iniD)
betaJ_notLB = newton(fB,betaJ_iniB)

print(betaJ_notLD)
print(betaJ_notLB)

def graf(betaD,betaB):
    fig = plt.figure(figsize=(13, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    Dj_curva = [Dj(ti,betaD) for ti in range(9)]
    Bj_curva = [Bj(ti,betaB) for ti in range(9)]
    
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
    

graf(betaJ_notLD,betaJ_notLB)

def graf_function_fit():
    betaJ = np.linspace(-.05,.5,100)
    curva = [function_fit(betaJ_i) for betaJ_i in betaJ]
    
    plt.plot(betaJ,curva)
    plt.grid()
    
# graf_function_fit()
    
    