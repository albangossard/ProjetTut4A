import matplotlib
matplotlib.use('Agg')
from config import *
import json

options = [sys.argv[i+1] for i in range(len(sys.argv)-1)]

if 'k' in options:
    method = 'K'
if 'pc' in options:
    method = 'PC'
if 'N' in options:
    distribName = 'Norm'
if 'U' in options:
    distribName = 'Unif'
if 'global' in options:
    global_compare='_glob'
    list_gamme=[0,1,2]
else:
    global_compare=''
    list_gamme=[-1,0,1,2]
if 'indS' in options:
    indice = 'S'
else:
    indice = 'S_T'

list_choice=[0,1,2]
# list_gamme=[-1,0,1,2]

for gamme in list_gamme:

    list_sobolKs=[]
    list_sobolQ=[]
    for choice in list_choice:
        if gamme==-1:
            fileName='sensAnalysis_'+distribName+'_choice='+str(choice)+'/uq'+method+'/sensitivity.json'
        else:
            fileName='sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'/uq'+method+'/sensitivity.json'
        with open(fileName) as jsonData:
            data=json.load(jsonData)
            list_sobolKs.append(data[indice+'_Ks'][0][0])
            list_sobolQ.append(data[indice+'_Q'][0][0])
    print("list_x="+str(list_x))
    print("list_sobolKs="+str(list_sobolKs))
    print("list_sobolQ="+str(list_sobolQ))

    plt.scatter(list_x, list_sobolKs, marker='o', label='Ks')
    plt.scatter(list_x, list_sobolQ, marker='*', label='Q')
    plt.xlabel('curvilinear abscissa x (km)')
    if indice=='S_T':
        plt.ylabel('Sobol total indices')
    else:
        plt.ylabel('First order Sobol indices')
    plt.legend(loc=5)
    if gamme==-1:
        plt.savefig('plots/Sobol_indep_compare_3pts_'+method+'_'+distribName+global_compare+'.png', dpi=dpi_plot)
    else:
        plt.savefig('plots/Sobol_indep_compare_3pts_'+method+'_'+distribName+global_compare+'_gamme='+str(gamme)+'.png', dpi=dpi_plot)
    plt.clf()