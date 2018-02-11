from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

list_init_size=[10,20,50,100,200]

for init_size in list_init_size:
    structOut["space"]["sampling"]["init_size"]=init_size
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='init_size='+str(init_size))
plt.legend()
plotInfo(plt,simul.getParamInText())
plt.xlabel("X")
plt.ylabel("h")
plt.savefig("plot/"+os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())+".png",dpi=500)
plt.show()
