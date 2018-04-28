import json
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as scs

from itertools import cycle
cycol = cycle('bgrcmk')

def gaussian(x, mu, sig):
    return np.exp(-(x-mu)**2./(2.*sig**2.))/(sig*np.sqrt(2.*np.pi))

list_choice=[0,1,2]
gamme=-1

list_x=np.array([437454, 425697, 412291])/10000.
for choice in list_choice:
    color=next(cycol)
    if gamme==-1:
        fileName='sensAnalysis_choice='+str(choice)+'/uqK/pdf.json'
    else:
        fileName='sensAnalysis_gamme='+str(gamme)+'_choice='+str(choice)+'/uqK/pdf.json'
    with open(fileName) as jsonData:
        data=json.load(jsonData)
        xAxis = np.array(data['output'][0])
        pdf = np.array(data['PDF'][0])
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
if gamme==-1:
    plt.savefig('PDF_indep_compare_3pts.png', dpi=200)
else:
    plt.savefig('PDF_indep_compare_3pts_gamme='+str(gamme)+'.png', dpi=200)
plt.show()
