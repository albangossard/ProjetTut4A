from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

# list_strategy=["Quad","LS"]
# list_strategy=["LS"]
list_strategy=["Quad"]

distrib=["BetaMuSigma(37.5, 5., 15., 60.).getDistribution()", "BetaMuSigma(4035, 400, 2500, 6000).getDistribution()"]
structOut["space"]["sampling"]["distributions"]=distrib

structOut["space"]["sampling"]["init_size"]=10*0+20*0+5
structOut["surrogate"]["degree"]=2*0+1*0+2*0+1

for strategy in list_strategy:
    structOut["surrogate"]["strategy"]=strategy
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    print("Q2="+str(simul.getQ2()))
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='strategy='+str(strategy))
plt.legend()
plotInfo(plt,simul.getParamInText())
plt.xlabel("Abscisse X (m)")
plt.ylabel("Water level h (m)")
plt.title("Water level along the abscisse")
plt.show()
