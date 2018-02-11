from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

list_tolerance=[0.9,0.95,0.99,0.999]

for tolerance in list_tolerance:
    structOut["pod"]["tolerance"]=tolerance
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='tolerance='+str(tolerance))
plt.legend()
plotInfo(plt,simul.getParamInText())
plt.xlabel("X")
plt.ylabel("h")
plt.savefig("plot/"+os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())+".png",dpi=500)
plt.show()
