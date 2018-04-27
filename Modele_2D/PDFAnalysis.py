import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scs
import statsmodels.api as sm

list_choice=[0,1,2]
gamme=-1

loi='Normale'
# loi='Lognormale'

nb=10000
uniform_distrib=np.random.uniform(size=nb)

list_x=np.array([437454, 425697, 412291])/10000.
for choice in list_choice:
    if gamme==-1:
        fileName='sensAnalysis_choice='+str(choice)+'/uqK/pdf.json'
    else:
        fileName='sensAnalysis_gamme='+str(gamme)+'_choice='+str(choice)+'/uqK/pdf.json'
    with open(fileName) as jsonData:
        data=json.load(jsonData)
        xAxis = np.array(data['output'][0])
        pdf = np.array(data['PDF'][0])
    cdf = np.zeros(pdf.shape)
    cdf[0] = pdf[0]
    for i in range(1,pdf.shape[0]):
        cdf[i]=cdf[i-1]+pdf[i]
    cdf/=np.max(cdf)
    plt.plot(pdf)
    plt.plot(cdf)
    plt.show()
    tab_val=np.zeros(uniform_distrib.shape[0])
    for i,e in enumerate(uniform_distrib):
        id_max=np.where(cdf<=e)[0][-1]
        val=xAxis[id_max]
        tab_val[i]=val
    if loi=='Lognormale':
        tab_val=np.exp(tab_val)
    """plt.hist(tab_val, bins=50)
    plt.show()"""
    tab_val_normalized=(tab_val-np.mean(tab_val))/np.std(tab_val)
    sm.qqplot(tab_val_normalized, line='45')
    if gamme==-1:
        plt.savefig('QQplot_'+str(loi)+'_choice='+str(choice)+'.png', dpi=200)
    else:
        plt.savefig('QQplot_gamme='+str(gamme)+'_'+str(loi)+'_choice='+str(choice)+'.png', dpi=200)
    plt.show()
    print("kurtosis="+str(scs.kurtosis(tab_val)))
