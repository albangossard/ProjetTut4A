import matplotlib
matplotlib.use('Agg')
from config import *
import json
import scipy.stats as scs
from itertools import cycle
cycol = cycle('bgrcmk')

options = [sys.argv[i+1] for i in range(len(sys.argv)-1)]

if 'k' in options:
    method = 'K'
if 'pc' in options:
    method = 'PC'
if 'N' in options:
    distribName = 'Norm'
if 'U' in options:
    distribName = 'Unif'

list_choice=[0,1,2]
list_gamme=[-1,0,1,2]

def gaussian(x, mu, sig):
    return np.exp(-(x-mu)**2./(2.*sig**2.))/(sig*np.sqrt(2.*np.pi))

for gamme in list_gamme:
    uniform_distrib=np.random.uniform(size=nb_pts_generation_distrib)
    for choice in list_choice:
        color=next(cycol)
        if gamme==-1:
            fileName='sensAnalysis_'+distribName+'_choice='+str(choice)+'/uq'+method+'/pdf.json'
        else:
            fileName='sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'/uq'+method+'/pdf.json'
        with open(fileName) as jsonData:
            data=json.load(jsonData)
            xAxis = np.array(data['output'][0])
            pdf = np.array(data['PDF'][0])
        
        cdf = np.zeros(pdf.shape)
        cdf[0] = pdf[0]
        for i in range(1,pdf.shape[0]):
            cdf[i]=cdf[i-1]+pdf[i]
        cdf/=np.max(cdf)
        tab_val=np.zeros(uniform_distrib.shape[0])
        for i,e in enumerate(uniform_distrib):
            tab_pos=np.where(cdf<=e)[0]
            if len(tab_pos)!=0:
                id_max=tab_pos[-1]
                val=xAxis[id_max]
            else:
                val=xAxis[0]
            tab_val[i]=val
        mean = np.mean(tab_val)
        std = np.std(tab_val)
        
        print("mean="+str(mean))
        print("std="+str(std))
        xGauss=np.linspace(xAxis.min(),xAxis.max(),200)
        yGauss=gaussian(xGauss, mean, std)
        plt.plot(xAxis,pdf,c=color,label='x='+str(list_x[choice]))
        plt.plot(xGauss,yGauss,'.',c=color)
    plt.xlabel('h(Ks,Q)')
    plt.ylabel('PDF')
    plt.legend()
    if gamme==-1:
        plt.savefig('plots/PDF_indep_compare_3pts_'+method+'_'+distribName+'.png', dpi=dpi_plot)
    else:
        plt.savefig('plots/PDF_indep_compare_3pts_'+method+'_'+distribName+'_gamme='+str(gamme)+'.png', dpi=dpi_plot)
    plt.clf()