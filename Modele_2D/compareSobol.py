import json
import numpy as np
import matplotlib.pyplot as plt

list_choice=[0,1,2]
list_gamme=[-1,0,1,2]
dists=['Uniform(17., 45.)','Normal(5750., 2075.)']; distribName='Norm'
# dists=['Uniform(17., 45.)','Uniform(1600., 9900.)']; distribName='Unif'

# indice='S'
indice='S_T'

# list_x=np.array([437454, 425697, 412291])/10000.
list_x=np.array([22., 36., 62.])

for gamme in list_gamme:

    list_sobolKs=[]
    list_sobolQ=[]
    for choice in list_choice:
        if gamme==-1:
            fileName='sensAnalysis_'+distribName+'_choice='+str(choice)+'/uqK/sensitivity.json'
        else:
            fileName='sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'/uqK/sensitivity.json'
        with open(fileName) as jsonData:
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
    plt.legend(loc=5)
    if gamme==-1:
        plt.savefig('plots/Sobol_indep_compare_3pts_'+distribName+'.png', dpi=200)
    else:
        plt.savefig('plots/Sobol_indep_compare_3pts_'+distribName+'_gamme='+str(gamme)+'.png', dpi=200)
    # plt.show()
    plt.clf()