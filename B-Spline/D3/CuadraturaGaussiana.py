import numpy as np
import matplotlib.pyplot as plt
from InterpocacionAcademicos import D_spline
from scipy.integrate import quad

F = np.array([69,0,19,49,18,29,26,87,83,90])
D = np.array([598,580,636,597,598,626,637,608,585,586])
B = np.array([75,123,175,249,313,338,363,506,632,740])
B_no_acum = np.array([75,48,52,74,64,25,25,143,126,108])

N = len(D)
def Cuad_array(arr): 
    return (-arr[0] + arr[-1])*(1/2) + sum(arr[:-1]) 

def Beta(i):
    SD = np.array([quad(D_spline,0,i) for i in range(N)]).T[0].astype(int)#[:-1]
    print("SD: ",SD)
    if i == 2:
        RB = B-B[0]
        # print("RB: ",RB)
        return (RB.T@SD)/(SD.T@SD)

    elif i == 1:
        R = (F-F[0])-(D-D[0])[:N] # = RF - RD
        # print("R: ",R)
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
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    D_curva_d = [Df(ti,betaD) for ti in range(N)]
    B_curva_b = [Bf(ti,betaB) for ti in range(N)]
    
    ax1.plot(D_curva_d,label = "Docentes sesgado a Docentes")
    ax2.plot(B_curva_b,label = "Docentes sesgado a Bajas")
    
    ax1.scatter(range(N),D,label = "Datos Docentes",color = "b")
    ax2.scatter(range(N),B,label = "Datos Bajas",color = "r")
    
    rango = (0,10)
    
    # Dlim = [min(D)-10,max(D)+10]
    # Blim = [min(B)-10,max(B)+10]
    # ax1.set_ylim(min(Dlim),max(Dlim))
    # ax2.set_ylim(min(Blim),max(Blim))    
    ax1.set_xlim(rango)
    ax2.set_xlim(rango)
    ax1.legend(loc = "upper left")
    ax2.legend(loc = "upper left")
    ax1.grid()
    ax2.grid()
    ax1.set_xticks(range(0,10),labels=range(2015,2025))
    ax2.set_xticks(range(0,10),labels=range(2015,2025))
    
graf()