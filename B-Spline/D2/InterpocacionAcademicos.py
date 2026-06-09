import numpy as np
import matplotlib.pyplot as plt
from BSpline_recursivo import B

## Datos ##

D = np.array([96,73,78])
N = len(D)

## Parámetros ##
# 2 + 4 - 3 = 3
t_inter = list(np.linspace(0,2,2))
k = 3 #orden
t = np.array(((k-1)*[t_inter[0]])+t_inter+((k-1)*[t_inter[-1]])) #vector de nodos
n = len(t)-k #cantidad de funciones básicas

## Ejecución ##

Base = [B(i,t,k) for i in range(n)]

M = np.array([[Base[i](ti) for i in range(n)] for ti in range(N)])

D_params = np.linalg.solve(M,D)

def D_spline(t):
    return D_params.T@np.array([Base[i](t) for i in range(n)])

## prints ##
# print("nodos: ", np.round(t,2))
# print("n: ",n,"\n")
# print("M: \n",np.round(M,2),"dim=",M.shape)
# print("Parametros: ",np.round(D_params,2))

## Graficar ##

def graf_D(intervalo):
    curva = [D_spline(t) for t in intervalo]
    
    plt.plot(intervalo,curva,label="Docentes B-spline",color = "green")
    plt.scatter(range(N), D,label="Docentes datos")
    
    plt.legend()
    plt.grid()
    plt.ylim(65,105)
    plt.xticks(range(N),range(2023,2026))


intervalo = np.linspace(t[0],t[-1], 100)
# graf_D(intervalo)













