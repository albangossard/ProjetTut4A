from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

list_method=["halton","uniform","lhs","faure","sobol","saltelli"]

for method in list_method:
    structOut["space"]["sampling"]["method"]=method
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='method='+str(method))
plt.legend()
plotInfo(plt,simul.getParamInText())
plt.xlabel("X")
plt.ylabel("h")
plt.savefig("plot/"+os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())+".png",dpi=500)
plt.show()
