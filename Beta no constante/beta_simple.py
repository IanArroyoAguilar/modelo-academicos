import numpy as np
import matplotlib.pyplot as plt

D = np.array([1912,1846,1844,1996,2099,2154,2110,2122,1917])
B = np.array([226, 449, 713, 927, 1085, 1279, 1437, 1629, 1852])

def cuad(t0,t1):
    return t0 + (t1-t0)/2

beta_bajas = [(B[ti+1] - B[ti])/(cuad(D[ti+1], D[ti]))    for ti in range(8)]

print(beta_bajas)

for i in range(8):
    plt.plot([i,i+1],[beta_bajas[i],beta_bajas[i]],color = "green")
    plt.scatter([i,i+1], 2*[beta_bajas[i]], color = "green",s=60)
    plt.text(((2*i+1)/2) - .09, beta_bajas[i]+.004, r"$\beta_"+str(i)+"$",size="x-large")
    if i == 7:
        continue
    else:
        plt.scatter([i+1], [beta_bajas[i]], color = "white",s=10)
    
plt.grid()
plt.ylim(.05,.2)
plt.xticks(range(9),range(2014,2023))
plt.title(r"$\beta$(t) como función simple")