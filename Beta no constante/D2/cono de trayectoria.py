import numpy as np
import matplotlib.pyplot as plt

def Cuad_array(arr): 
    return (-arr[0] + arr[-1])*(1/2) + sum(arr[:-1])

def cuad(t0,t1,dt):
    return dt*(t0 + t1)/2

D = np.array([598,580,636,597,598,626,637,608,585,586])
F = np.array([69,0,19,49,18,29,26,87,83,90])
N = len(F)
B_no_acum = np.array([75,48,52,74,64,25,25,143,126,108])
B = np.array([sum(B_no_acum[:i+1]) for i in range(N)])

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














