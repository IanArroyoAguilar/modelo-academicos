import numpy as np
import matplotlib.pyplot as plt 
from scipy.optimize import newton
from scipy.optimize import fsolve

# DATOS #
B = [226, 449, 713, 927, 1085, 1279, 1437, 1629, 1852]
D = [1912,1846,1844,1996,2099,2154,2110,2122,1917]
F = [227,301,325,407,490,546,517,509,571,571+31,571+57,571+99]
#                                       | datos nuevos a partir de: |
año_final = len(F)




def F_func(t):
    """Para obtener una división mensual de los 9 años 
    evaluar la función en 97 puntos distribuidos de manera uniforme en el intervalo [0,8]
    En el caso general de que sea hasta el año a se utilizan: 
                    cp = 12*(año_final-1) + 1
    puntos tomados de manera uniforme en el intervalo [0,a-1]"""
    for ti in range(1,año_final):
        if t >= ti-1 and t <= ti:
            return (F[ti] - F[ti-1])*(t-(ti-1)) + F[ti-1]
        
        
cp= 12*(año_final-1) + 1
t_split = np.linspace(0, año_final-1,cp)
print(t_split)
# print(t_split)
# F_t_split = [F_func(t_split[i]) for i in range(cp)]

# CUADRATURA #
def C(t,b):
    """Cuadratura de la funcion f evaluada en el, los parámetros en b desde 0 hasta tN"""
    FulArr = np.array([Fe(t, b) for t in t_split[t_split<=t]])
    # print("c: ",((FulArr[-1] - FulArr[0])/2) + sum(FulArr))
    return np.float64(((FulArr[-1] - FulArr[0])/2) + sum(FulArr))*(1/12)

# FUNCIONES INTERMEDIAS #

def Fe(tN,b):
    """Se usa en practicamente todas las  funciones"""
    return np.float64(F_func(tN)*(np.e**(tN*b)))

def F_Ac1(tN,b):
    return D[0] - F[0] - b*C(tN, b)

def F_Ac(tN,b):
    return (np.e**(-tN*b))*(F_Ac1(tN,b))
    

# FUNCIONES DE DOCENTES Y BAJAS #   
def Doc(tN,b):
    return F_func(tN) + F_Ac(tN, b)
    
def Bajas(tN,b):
    return B[0] - F_Ac(tN, b) + D[0] - F[0]    

def graficar_doc():
    fig = plt.figure(figsize=(12, 5))
    ax3 = fig.add_subplot(121)
    ax1 = fig.add_subplot(122)
    
    ax3.scatter(range(9),F[:9],label = "Datos")
    ax3.scatter(range(9,12),F[9:],label = "Simulado",color="red")
    ax1.scatter(range(9),D,label = "Datos")
      
    oldt = t_split[t_split<=8]
    newt = t_split[t_split>=8]
    
    D_curva_old = np.array([Doc(ti,beta_opt[0]) for ti in oldt])
    B_curva_old = np.array([Bajas(ti,beta_opt[1]) for ti in oldt])
    
    D_curva_new = np.array([Doc(ti,beta_opt[0]) for ti in newt])
    B_curva_new = np.array([Bajas(ti,beta_opt[1]) for ti in newt]) 
   
    ax1.plot(oldt,D_curva_old,label = "Ajuste",color="blue")
    
    ax1.plot(newt,D_curva_new,label = "Predicción",color="red",linestyle="dotted",linewidth=4)
    
    
    ax1.set_title(label="Académicos")
    ax3.set_title(label="Entrada de personal")
    ax1.set_ylim(min(D)-100,max(D)+50)
    ax1.set_xlim(-1,12)
    ax1.legend(loc="lower right")
    ax3.legend(loc="lower right")
    ax1.set_xticks(range(-1,12,2),labels=range(2013,2026,2))
    ax3.set_xticks(range(-1,12,2),labels=range(2013,2026,2))
    ax1.grid()
    ax3.grid()
    
beta_opt = [0.01269695, 0.14795897]


graficar_doc()