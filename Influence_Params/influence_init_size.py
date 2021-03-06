from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

list_init_size=[5,10,15,20,50]

distrib=["BetaMuSigma(37.5, 5., 15., 60.).getDistribution()", "BetaMuSigma(4035, 400, 2500, 6000).getDistribution()"]

structOut["surrogate"]["method"]="kriging"
structOut["surrogate"]["strategy"]="LS"
structOut["space"]["sampling"]["distributions"]=distrib

for init_size in list_init_size:
    structOut["space"]["sampling"]["init_size"]=init_size
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='init_size='+str(init_size))
plt.legend()
# plotInfo(plt,simul.getParamInText())
plt.xlabel("Abscisse X (m)")
plt.ylabel("Water level h (m)")
plt.title("Water level along the abscisse")
fileName=os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())
plt.savefig("plot/"+fileName+".png",dpi=500)
simul.saveSettings("plot/"+fileName+".json")
# plt.show()
