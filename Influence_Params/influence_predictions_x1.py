from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

list_predictions=[[15,4000],[20,4000],[25,4000],[30,4000],[35,4000],[40,4000],[45,4000],[50,4000],[55,4000],[60,4000]]
# list_predictions=[[15,4000],[20,4000]]

# structOut["space"]["sampling"]["init_size"]=20

structOut["surrogate"]["predictions"]=list_predictions
simul=batmanIO('',structOut)
simul.run()
simul.read()
X=simul.getSpacePts()
x1,x2,F=simul.getDataOut()
for i,predictions in enumerate(list_predictions):
    plt.plot(X,F[i],label='predictions='+str(predictions))
plt.legend()
plotInfo(plt,simul.getParamInText())
plt.xlabel("X")
plt.ylabel("h")
plt.savefig("plot/"+os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())+".png",dpi=500)
plt.show()
