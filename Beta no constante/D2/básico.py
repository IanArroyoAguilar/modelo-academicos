import numpy as np
import matplotlib.pyplot as plt

def Cuad_array(arr): 
    return (-arr[0] + arr[-1])*(1/2) + sum(arr[:-1])

def cuad(t0,t1,dt):
    return dt*(t0 + t1)/2

D = np.array([96,73,78])
F = np.array([10,7,17])
B = np.array([22,32,39])
B_no_acum = np.array([22,10,7])

N = min(len(B), len(F), len(D))

def Betas(sesgo):
    baj = np.array([(B[ti+1]-B[ti])/cuad(D[ti], D[ti+1],1) for ti in range(N-1)])
    doc = np.array([((F[ti+1]-F[ti])-(D[ti+1]-D[ti]))/cuad(D[ti], D[ti+1],1) for ti in range(N-1)])

    return {"bajas":baj,"docentes":doc}[sesgo]

def A(k,t,beta):
    return F[t] + (np.e**(-beta[k]*(t-k)))*(D[k]-F[k] - beta[k]*cuad(F[k],F[t]*(np.e**(beta[k]*(t-k))),t-k))

def Baj(k,t,beta):
    return B[k] + beta[k]*cuad(A(k,t,beta),A(k,t,beta),t-k)

r = [A,Baj]

def graf():
    fig = plt.figure()
    ax = [fig.add_subplot(121), fig.add_subplot(122)]
    
    ax[0].scatter(range(N),D,color="green",label="Datos Académicos")
    ax[1].scatter(range(N),B,color="red",label="Datos Bajas")
    
    sesgo = ["docentes","bajas"]
    
    for s in [0,1]:
        b = Betas(sesgo[s])
        print(np.round(b,3))
        for k in range(N-1):
            points = [r[s](k,k,b),r[s](k,k+1,b)]
            ax[s].plot([k,k+1],points,color="blue")
        
        ax[s].grid()
        ax[s].legend()    
        ax[s].set_xticks(range(N),range(2022,2022+N))
    




graf()
