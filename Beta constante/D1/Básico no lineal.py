import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

# Datos
B = np.array([226, 449, 713, 927, 1085, 1279, 1437, 1629, 1852])
D = np.array([1912,1846,1844,1996,2099,2154,2110,2122,1917])
F = np.array([227,301,325,407,490,546,517,509,571])

# Valores iniciales
beta_iniD, beta_iniB = 0.19277376544012045, 0.10382374483431064

# Funciones auxiliares
def Cuad_array(arr,t): 
    return (-arr[0] + arr[t])*(1/2) + sum(arr[:t]) 

def Fe(t,beta):
    return F[t]*np.exp(t*beta)

def Fez(t,beta):
    return t*F[t]*np.exp(t*beta)

def Df(t,beta):
    return F[t] + np.exp(-t*beta)*(D[0] - F[0] - beta*Cuad_array(Fe(np.arange(0,t+1),beta),t))

def Bf(t,beta):    
    return B[0] + beta*Cuad_array(np.array([Df(ti,beta) for ti in range(9)]), t)

# Residuales
def residualsD(beta):
    return np.array([D[ti] - Df(ti,beta) for ti in range(9)]).ravel()

def residualsB(beta):
    return np.array([B[ti] - Bf(ti,beta) for ti in range(9)]).ravel()

# Jacobianos (vector columna)
def JD(beta):
    # derivada de los residuales respecto a beta
    J = []
    for ti in range(9):
        FD = D[0] - F[0] - beta*Cuad_array(Fe(np.arange(0,ti+1),beta),ti)
        dFD = -Cuad_array(Fe(np.arange(0,9),beta), ti) - beta*Cuad_array(Fez(np.arange(0,9),beta), ti)
        dD = -ti*np.exp(-ti*beta)*FD + dFD*np.exp(-ti*beta)
        J.append(-dD)  # signo negativo porque residual = dato - modelo
    return np.array(J)

def JB(beta):
    J = []
    for ti in range(9):
        dD_vals = []
        for tj in range(9):
            FD = D[0] - F[0] - beta*Cuad_array(Fe(np.arange(0,tj+1),beta),tj)
            dFD = -Cuad_array(Fe(np.arange(0,9),beta), tj) - beta*Cuad_array(Fez(np.arange(0,9),beta), tj)
            dD_vals.append(-tj*np.exp(-tj*beta)*FD + dFD*np.exp(-tj*beta))
        dB = Cuad_array(np.array([Df(tj,beta) for tj in range(9)]), ti) + Cuad_array(np.array(dD_vals), ti)
        J.append(-dB)
    return np.array(J)

# Ajuste con LM
beta_notLD = least_squares(residualsD, beta_iniD, jac=JD, method="lm")
beta_notLB = least_squares(residualsB, beta_iniB, jac=JB, method="lm")

print("Beta Docentes:", beta_notLD.x[0])
print("Beta Bajas:", beta_notLB.x[0])

# Gráfico
def graf(betaD,betaB):
    fig = plt.figure(figsize=(13, 6))
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    
    D_curva = [Df(ti,betaD) for ti in range(9)]
    B_curva = [Bf(ti,betaB) for ti in range(9)]
    
    ax1.plot(range(9),D_curva,label='Dj función')
    ax1.scatter(range(9),D,label='Dj datos')
    
    ax2.plot(range(9),B_curva,label='Bj función')
    ax2.scatter(range(9),B,label='Bj datos')
    
    ax1.set_xticks(range(9),range(2014,2023))
    ax2.set_xticks(range(9),range(2014,2023))
    ax1.set_title('Docentes')
    ax2.set_title('Bajas')
    ax1.grid() 
    ax2.grid()
    plt.show()

graf(beta_notLD.x[0], beta_notLB.x[0])