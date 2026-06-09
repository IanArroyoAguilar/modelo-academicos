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


def Betas(sesgo,D_fic,B_fic):
    N = min(len(B_fic), len(D_fic))
    baj = np.array([(B_fic[ti+1]-B_fic[ti])/cuad(D_fic[ti], D_fic[ti+1],1) for ti in range(N-1)])
    doc = np.array([((F[ti+1]-F[ti])-(D_fic[ti+1]-D_fic[ti]))/cuad(D_fic[ti], D_fic[ti+1],1) for ti in range(N-1)])

    return {"bajas":baj,"docentes":doc}[sesgo]

def A(k,t,beta,D_fic):
    return F[t] + (np.e**(-beta*(t-k)))*(D_fic[k]-F[k] - beta*cuad(F[k],F[t]*(np.e**(beta*(t-k))),t-k))

def Baj(k,t,beta,D_fic,B_fic):
    return B_fic[k] + beta*cuad(A(k,k,beta,D_fic),A(k,t,beta,D_fic),t-k)


def graf(last):
    D_usable = np.array([96,73,78][:-last])
    B_usable = np.array([22,32,39][:-last])
    
    fig = plt.figure()
    ax = [fig.add_subplot(121), fig.add_subplot(122)]
    
    ax[0].scatter(range(N),D,color="green",label="Datos Académicos")
    ax[1].scatter(range(N),B,color="red",label="Datos Bajas")
    
    #docentes    
    
    b = Betas("docentes",D_usable,B_usable)
    print("\n\t Docentes: "+"\n")
    
    for k in range(N-1)[:-last]:
        if k < N-1-last:
            first, second = A(k,k,b[k],D_usable),A(k,k+1,b[k],D_usable)
            print("modelo: ",np.round(second,3)," ~ Valor Real: ",D[k+1])
            ax[0].plot([k,k+1],[first, second],color="blue")
    Dnew = []    
    print("\n  Predicción")       
    for k in range(N-1-last,N-1):
            D_fic = list(D_usable)+Dnew
            b = Betas("docentes", D_fic, D_fic)
            first, second = A(k,k,b[k-1], D_fic),A(k,k+1,b[k-1], D_fic)
            Dnew.append(second)
            print("modelo: ",np.round(second,3)," ~ Valor Real: ",D[k+1])
            ax[0].plot([k,k+1],[first,second],color="blue",linestyle = "--")
    
    D_usable = D_fic+[second]
    #bajas    
    
    b = Betas("bajas",D_usable,B_usable)
    print("\n\t Bajas: "+"\n")
    
    for k in range(N-1)[:-last]:
        if k < N-1-last:
            first, second = Baj(k,k,b[k],D_usable,B_usable),Baj(k,k+1,b[k],D_usable,B_usable)
            print("modelo: ",np.round(second,3)," ~ Valor Real: ",B[k+1])
            ax[1].plot([k,k+1],[first, second],color="blue")
    Bnew = []   
    print("\n  Predicción")        
    for k in range(N-1-last,N-1):
            B_fic = list(B_usable)+Bnew
            b = Betas("bajas", D_usable, B_fic)
            first, second = Baj(k,k,b[k-1],D_usable,B_fic),Baj(k,k+1,b[k-1],D_usable,B_fic)
            Bnew.append(second)
            print("modelo: ",np.round(second,3)," ~ Valor Real: ",B[k+1])
            ax[1].plot([k,k+1],[first,second],color="blue",linestyle = "--")        
    
    
    for s in [0,1]:
        ax[s].grid()
        ax[s].legend()    
        ax[s].set_xticks(range(N),range(2014,2014+N))

# El parámetro indica la cantidad de datos que se eliminan
# de la información disponible de académicos y bajas.
# Es decir, la cantidad de años que se intentan predecir.

# Se utiliza solamente la ultima beta en la predicción
# Al hacer la predicción se usa ese valor para calcular la
# siguiente beta y así sucesivamente.
    
graf(1)

