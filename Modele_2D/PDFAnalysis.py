import matplotlib
matplotlib.use('Agg')
from config import *
import json
import scipy.stats as scs
import statsmodels.api as sm

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
# list_loi=['Normale', 'Lognormale']
list_loi=['Normale']

for loi in list_loi:
    for gamme in list_gamme:
        uniform_distrib=np.random.uniform(size=nb_pts_generation_distrib)
        for choice in list_choice:
            if gamme==-1:
                fileName='sensAnalysis/sensAnalysis_'+distribName+'_choice='+str(choice)+'/uq'+method+'/pdf.json'
            else:
                fileName='sensAnalysis/sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'/uq'+method+'/pdf.json'
            with open(fileName) as jsonData:
                data=json.load(jsonData)
                xAxis = np.array(data['output'][0])
                pdf = np.array(data['PDF'][0])
            cdf = np.zeros(pdf.shape)
            cdf[0] = pdf[0]
            for i in range(1,pdf.shape[0]):
                cdf[i]=cdf[i-1]+pdf[i]
            cdf/=np.max(cdf)
            # plt.plot(pdf)
            # plt.plot(cdf)
            # plt.show()
            tab_val=np.zeros(uniform_distrib.shape[0])
            for i,e in enumerate(uniform_distrib):
                tab_pos=np.where(cdf<=e)[0]
                if len(tab_pos)!=0:
                    id_max=tab_pos[-1]
                    val=xAxis[id_max]
                else:
                    val=xAxis[0]
                tab_val[i]=val
            if loi=='Lognormale':
                tab_val=np.exp(tab_val)
            """plt.hist(tab_val, bins=50)
            plt.show()"""
            tab_val_normalized=(tab_val-np.mean(tab_val))/np.std(tab_val)
            sm.qqplot(tab_val_normalized, line='45')
            if gamme==-1:
                plt.savefig('plots/QQplot_'+method+'_'+distribName+'_'+str(loi)+'_choice='+str(choice)+'.png', dpi=dpi_plot)
            else:
                plt.savefig('plots/QQplot_'+method+'_'+distribName+'_'+str(loi)+'_gamme='+str(gamme)+'_choice='+str(choice)+'.png', dpi=dpi_plot)
            plt.clf()
            print("kurtosis="+str(scs.kurtosis(tab_val)))
