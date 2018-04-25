import json
import numpy as np
import matplotlib.pyplot as plt

list_choice=[0,1,2]

# indice='S'
indice='S_T'

list_x=np.array([437454, 425697, 412291])/10000.
list_sobolKs=[]
list_sobolQ=[]
for choice in list_choice:
    with open('sensAnalysis_choice='+str(choice)+'/uqK/sensitivity.json') as jsonData:
        data=json.load(jsonData)
        list_sobolKs.append(data[indice+'_Ks'][0][0])
        list_sobolQ.append(data[indice+'_Q'][0][0])
print("list_x="+str(list_x))
print("list_sobolKs="+str(list_sobolKs))
print("list_sobolQ="+str(list_sobolQ))

plt.scatter(list_x, list_sobolKs, marker='o', label='Ks')
plt.scatter(list_x, list_sobolQ, marker='*', label='Q')
plt.xlabel('x (km)')
plt.ylabel('Sobol total indices')
plt.legend()
plt.savefig('Sobol_indep_compare_3pts.png', dpi=200)
plt.show()