from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

# list_degree=[5,10,15,20,50]
list_degree=[1,2,3]

distrib=["BetaMuSigma(37.5, 5., 15., 60.).getDistribution()", "BetaMuSigma(4035, 400, 2500, 6000).getDistribution()"]

# structOut["surrogate"]["method"]="kriging"
structOut["surrogate"]["strategy"]="Quad"
structOut["space"]["sampling"]["distributions"]=distrib

for degree in list_degree:
    structOut["surrogate"]["degree"]=degree
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='degree='+str(degree))
plt.legend()
# plotInfo(plt,simul.getParamInText())
plt.xlabel("Abscisse X (m)")
plt.ylabel("Water level h (m)")
plt.title("Water level along the abscisse")
fileName=os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())
plt.savefig("plot/"+fileName+".png",dpi=500)
simul.saveSettings("plot/"+fileName+".json")
# plt.show()
