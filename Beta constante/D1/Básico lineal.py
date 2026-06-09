import numpy as np
import matplotlib.pyplot as plt 


D = np.array([1912,1846,1844,1996,2099,2154,2110,2122,1917])
F = np.array([227,301,325,407,490,546,517,509,571])
B = np.array([226, 449, 713, 927, 1085, 1279, 1437, 1629, 1852])
B_no_acum = np.array([226, 223, 264, 214, 158, 194, 158, 192, 223])

n = 9
Sn = 9

print("Bajas artificiales acumuladas: ",B)

def Cuad_array(arr): 
    return (-arr[0] + arr[-1])*(1/2) + sum(arr[:-1]) 

def Beta(i):
    SD = np.array([((D[i]-D[0])/2) + sum(D[:i]) for i in range(Sn)])#[:-1]
    print("SD: ",SD)
    if i == 2:
        RB = B-B[0]
        print("RB: ",RB)
        return (RB.T@SD)/(SD.T@SD)

    elif i == 1:
        R = (F-F[0])-(D-D[0])[:Sn]# = RF - RD
        print("R: ",R)
        return (R.T@SD)/(SD.T@SD)

betaD,betaB = Beta(1),Beta(2)
# betaD,betaB = .01269695,.14795897

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
    
    rango = (-1,9)
    
    Dlim = [min(D)-50,max(D)+50]
    ax1.set_ylim(min(Dlim),max(Dlim))
    ax2.set_ylim(min(Dlim),max(Dlim))    
    ax1.set_xlim(rango)
    ax2.set_xlim(rango)
    ax1.legend(loc = "upper left")
    ax2.legend(loc = "upper left")
    ax1.set_xticks(range(-1,9),labels=range(2013,2023))
    ax2.set_xticks(range(-1,9),labels=range(2013,2023))
    
    Blim = max(B)+200
    ax3.set_ylim(0,Blim)
    ax4.set_ylim(0,Blim)    
    ax3.set_xlim(rango)
    ax4.set_xlim(rango)
    ax3.legend(loc = "upper left")
    ax4.legend(loc = "upper left")
    ax3.set_xticks(range(-1,9),labels=range(2013,2023))
    ax4.set_xticks(range(-1,9),labels=range(2013,2023))
    ax1.grid()
    ax2.grid()
    ax3.grid()
    ax4.grid()
    
graf()