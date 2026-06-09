import numpy as np
import matplotlib.pyplot as plt

def Cuad_array(arr): 
    return (-arr[0] + arr[-1])*(1/2) + sum(arr[:-1])

def cuad(t0,t1,dt):
    return dt*(t0 + t1)/2

D = np.array([1912,1846,1844,1996,2099,2154,2110,2122,1917])
F = np.array([227,301,325,407,490,546,517,509,571])
B = np.array([226, 449, 713, 927, 1085, 1279, 1437, 1629, 1852])
B_no_acum = np.array([226, 223, 264, 214, 158, 194, 158, 192, 223])

N = min(len(B), len(F), len(D))

def Betas(sesgo):
    baj = np.array([(B[ti+1]-B[ti])/cuad(D[ti], D[ti+1],1) for ti in range(N-1)])
    doc = np.array([((F[ti+1]-F[ti])-(D[ti+1]-D[ti]))/cuad(D[ti], D[ti+1],1) for ti in range(N-1)])

    return {"bajas":baj,"docentes":doc}[sesgo]

def A(k,t,beta):
    return F[t] + (np.e**(-beta[k]*(t-k)))*(D[k]-F[k] - beta[k]*cuad(F[k],F[t]*(np.e**(beta[k]*(t-k))),t-k))

def Baj(k,t,beta):
    return B[k] + beta[k]*cuad(A(k,t,beta),A(k,t,beta),t-k)



def graf(alphas):
    fig = plt.figure()
    ax = [fig.add_subplot(121), fig.add_subplot(122)]
    
    ax[0].scatter(range(N),D,color="green",label="Datos Académicos")
    ax[1].scatter(range(N),B,color="red",label="Datos Bajas")
    
    sesgo = ["docentes","bajas"]
    rf = [A,Baj]
    dd = [D,B]
    for s in [0,1]:
        betas = Betas(sesgo[s]), Betas(sesgo[s-1])
        
        for alpha in alphas:
            b = alpha*betas[0] + (1-alpha)*betas[1]
            # print(np.round(b,3))
            print(sesgo[s]+": \n")
            for k in range(N-1):
                points = [rf[s](k,k,b),rf[s](k,k+1,b)]
                print("modelo: ",np.round(rf[s](k,k+1,b),3)," ~ Valor Real: ",dd[s][k+1])
                ax[s].plot([k,k+1],points,color="blue")
                    
        ax[s].grid()
        ax[s].legend()    
        ax[s].set_xticks(range(N),range(2014,2014+N))
    
# En cada paso de la estimación se divide el cono
# de trayectorias basandose en los valores de alphas

graf(alphas = [0,.333,.6666,1])














