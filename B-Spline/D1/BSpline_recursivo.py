import numpy as np
import matplotlib.pyplot as plt

## Construcción de bases ##
div_noncero = lambda num,den: num/den if den > 1e-8 else 0

class B:
    def __init__(self,index,knots,order):
        self.i = index
        self.t = knots
        self.k = order
        
        self.base_function = self.f_0 if self.k == 1 else self.general_f
    
    def f_0(self,x):
        i,t = self.i, self.t
            
        return 1 if (t[i]<=x<=t[i+1]) else 0
    
    def general_f(self,x):
        i,t,k = self.i, self.t, self.k
        
        num1 = x - t[i]
        den1 = t[i + k - 1] - t[i]
        
        num2 = t[i+k] - x
        den2 = t[i + k] - t[i + 1]
        
        prev_base_i = B(i, t, k-1)
        prev_base_ip1 = B(i+1, t, k-1)
        
        term1 = div_noncero(num1, den1) * prev_base_i(x)
        term2 = div_noncero(num2, den2) * prev_base_ip1(x)
        
        return  term1 + term2
    
    def __call__(self,x):
        return self.base_function(x)

## Graficar ##
def graf(intervalo,Base):
    n = len(Base)
    curvas = np.array([np.array([Base[i](x) for x in intervalo]) for i in range(n)])
    # print(curvas)
    
    for i in range(n):
        plt.plot(intervalo,curvas[i],color=np.random.uniform(0,1,3),label=f"B_{i}")
    
## Parámetros ##
t = [0,.25,.5,.75,1]
k = 3 #orden
n = len(t)-k #cantidad de funciones básicas

## Ejecución ##
Base = np.array([B(i,t,k) for i in range(n)])

intervalo = np.linspace(t[0],t[-1], 1000)

# graf(intervalo,Base)

