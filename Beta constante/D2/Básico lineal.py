import numpy as np
import matplotlib.pyplot as plt 


D = np.array([96,73,78])
F = np.array([10,7,17])
B = np.array([22,32,39])
B_no_acum = np.array([22,10,7])

n = 3
Sn = 3

def Cuad_array(arr): 
    return (-arr[0] + arr[-1])*(1/2) + sum(arr[:-1]) 

def Beta(i):
    SD = np.array([((D[i]-D[0])/2) + sum(D[:i]) for i in range(Sn)])#[:-1]
    if i == 2:
        RB = B-B[0]
        return (RB.T@SD)/(SD.T@SD)

    elif i == 1:
        R = (F-F[0])-(D-D[0])[:Sn]# = RF - RD
        print("R: ",R)
        return (R.T@SD)/(SD.T@SD)

betaD,betaB = Beta(1),Beta(2)

print("Beta sesgada a docentes: ",betaD,"\t\tBeta sesgada a bajas: ",betaB)

def Fe(t,beta):
    return F[t]*(np.e**(t*(beta)))

def Df(t,beta):
    return F[t] + (np.e**(-t*(beta)))*(D[0]-F[0]-(beta)*Cuad_array(np.array([Fe(ti,beta) for ti in range(t+1)])))

def Bf(t,beta):
    return B[0] + beta*(Cuad_array(np.array([Df(ti,beta) for ti in range(t+1)])))

def graf():
    fig = plt.figure(figsize=(14, 9.5))
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)
    
    D_curva_d = [Df(ti,betaD) for ti in range(Sn)]
    D_curva_b = [Df(ti,betaB) for ti in range(Sn)]
    B_curva_d = [Bf(ti,betaD) for ti in range(Sn)]
    B_curva_b = [Bf(ti,betaB) for ti in range(Sn)]
    
    ax1.plot(D_curva_d,label = "Docentes sesgado a Docentes")
    ax2.plot(D_curva_b,label = "Docentes sesgado a Bajas")
    ax3.plot(B_curva_d,label = "Bajas sesgado a Docentes")
    ax4.plot(B_curva_b,label = "Bajas sesgado a Bajas")
    
    ax1.scatter(range(n),D,label = "Datos Docentes",color = "b")
    ax2.scatter(range(n),D,label = "Datos Docentes",color = "b")
    ax3.scatter(range(Sn),B,label = "Datos Bajas",color = "b")
    ax4.scatter(range(Sn),B,label = "Datos Bajas",color = "b")
    
    
    ax1.legend()
    ax2.legend()
    ax1.set_xticks(range(0,3),labels=range(2023,2026))
    ax2.set_xticks(range(0,3),labels=range(2023,2026))
    
    ax3.legend()
    ax4.legend()
    ax3.set_xticks(range(0,3),labels=range(2023,2026))
    ax4.set_xticks(range(0,3),labels=range(2023,2026))
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    
graf()