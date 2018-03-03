from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

list_method=["kriging","pc"]
list_Q2=[]

distrib=["Uniform(15., 60.)", "BetaMuSigma(4035, 400, 2500, 6000).getDistribution()"]

structOut["surrogate"]["strategy"]="Quad"
structOut["space"]["sampling"]["distributions"]=distrib

structOut["surrogate"]["degree"]=3

for method in list_method:
    structOut["surrogate"]["method"]=method
    print("Simul for method="+str(method))
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    Q2=simul.getQ2()
    list_Q2.append(Q2)
    print("Q2="+str(Q2))
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='method='+str(method))
list_method=np.array(list_method)
list_Q2=np.array(list_Q2)
plt.legend()
# plotInfo(plt,simul.getParamInText())
plt.xlabel("Abscisse X (m)")
plt.ylabel("Water level h (m)")
plt.title("Water level along the abscisse")
fileName=os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())
plt.savefig("plot/"+fileName+".png",dpi=500)
simul.saveSettings("plot/"+fileName+".json")
np.savetxt("plot/"+fileName+"_list_method.dat", list_method, fmt='%s')
np.savetxt("plot/"+fileName+"_list_Q2.dat", list_Q2)
plt.show()

plt.plot(list_method, list_Q2)
plt.show()
