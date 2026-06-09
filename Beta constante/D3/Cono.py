import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.gridspec as gridspec

#### Notas ####

# Estoy generando las baja a partir de los docentes y las altas.
# Regla usada D[ti] = D[ti-1] + F[ti] - B[ti]  <=> B[ti] = D[ti-1] + F[ti] - D[ti]
# No estoy utilizando el último punto en las altas y bajas

# Deficiones:  RA = A-A[0], SA = A[:-1] 

n = 10
Sn = 10

F = np.array([69,0,19,49,18,29,26,87,83,90])
D = np.array([598,580,636,597,598,626,637,608,585,586])
B = np.array([75,123,175,249,313,338,363,506,632,740])
B_no_acum = np.array([75,48,52,74,64,25,25,143,126,108])


alpha = [0,.05,.15,.25,.35,.45,.5,.55,.65,.75,.85,.95,1]
SD = np.array([((D[i]-D[0])/2) + sum(D[:i]) for i in range(Sn)])
RB = B-B[0]
R = (F-F[0])-(D-D[0])


def Cuad_array(arr): 
    return (-arr[0] + arr[-1])*(1/2) + sum(arr[:-1]) 


def Beta(a):
    return (SD.T@(a*R + (1-a)*RB))/(SD.T@SD)
        
def Fe(t,beta):
    return F[t]*(np.e**(t*(beta)))

def Df(t,beta):
    return F[t] + (np.e**(-t*(beta)))*(D[0]-F[0]-(beta)*Cuad_array(np.array([Fe(ti,beta) for ti in range(t+1)])))

def Bf(t,beta):
    return B[0] + beta*(Cuad_array(np.array([Df(ti,beta) for ti in range(t+1)])))

def graf():
    fig = plt.figure(figsize=(13.5, 6))
    gs = gridspec.GridSpec(1,3,width_ratios=[3,3,1.5])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])
    ax3.axis("off")
    
    
    ax1.scatter(range(n),D,label = "Datos Docentes",color = "black")
    ax2.scatter(range(n),B,label = "Datos Bajas",color = "black")
    
    c = np.array([1,0,0]).astype(float)
    for i in range(len(alpha)):
        if alpha[i] <= .5:
            c[1] = 2*alpha[i]
        else:
            c[0] = 2*(1-alpha[i])
        # print(c)
        # c = (1-alpha[i])*np.array([1,0,0]) + alpha[i]*np.array([1,1,0]) + alpha[i]*np.array([0,1,0])
        # c = (1-alpha[i])*np.array([1,0,0]) + 2*alpha[i]*np.array([1,1,0]) 
        # c = (1-alpha[i])*np.array([1,0,1]) + alpha[i]*np.array([1,0,0])
        beta = Beta(alpha[i])
        print(beta)
        D_curva_d = [Df(ti,beta) for ti in range(Sn)]
        B_curva_b = [Bf(ti,beta) for ti in range(Sn)]
    
        ax1.plot(D_curva_d,color = c.astype(float))
        ax2.plot(B_curva_b,color = c.astype(float))
        ax3.plot([0],[0],label = "Sesgo: "+str(alpha[i])+"B + "+str(round(1-alpha[i],2))+"D",color = c.astype(float))
    
    
    
    ax1.legend()
    ax2.legend()
    ax3.legend()
    ax1.set_xticks(range(10),labels=range(2015,2025))
    ax2.set_xticks(range(10),labels=range(2015,2025))
    ax1.grid()
    ax2.grid()
    plt.tight_layout()
    
graf()