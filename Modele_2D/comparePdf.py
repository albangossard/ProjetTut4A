import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scs

from itertools import cycle
cycol = cycle('bgrcmk')

def gaussian(x, mu, sig):
    return np.exp(-(x-mu)**2./(2.*sig**2.))/(sig*np.sqrt(2.*np.pi))

list_choice=[0,1,2]

list_x=np.array([437454, 425697, 412291])/10000.
list_sobolKs=[]
list_sobolQ=[]
for choice in list_choice:
    color=cycol.next()
    with open('sensAnalysis_choice='+str(choice)+'/uqK/pdf.json') as jsonData:
        data=json.load(jsonData)
        xAxis = np.array(data['output'][0])
        pdf = np.array(data['PDF'][0])
    # print("kurtosis="+str(scs.kurtosis(pdf))) # NE MARCHE PAS DU TOUT -> VOIR EXPLICATION PAPIER
    # mean=np.mean(data)
    delta=xAxis[1]-xAxis[0]
    mean=np.sum(np.multiply(xAxis,pdf))*delta
    print("mean="+str(mean))
    std=np.sqrt(np.sum(np.multiply((xAxis-mean)**2.,pdf))*delta)
    print("std="+str(std))
    xGauss=np.linspace(xAxis.min(),xAxis.max(),200)
    yGauss=gaussian(xGauss, mean, std)
    plt.plot(xAxis,pdf,c=color,label='x='+str(list_x[choice]))
    plt.plot(xGauss,yGauss,'.',c=color)
    # for percentile in np.linspace(0,100,50):
    #     quant=np.percentile(yGauss)
plt.xlabel('h(Ks,Q)')
plt.ylabel('PDF')
plt.legend()
plt.savefig('PDF_indep_compare_3pts.png', dpi=200)
plt.show()
