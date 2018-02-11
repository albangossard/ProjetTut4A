from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime


structOut["space"]["sampling"]["init_size"]=10
simul=batmanIO('',structOut)
simul.run()
simul.read()
X=simul.getSpacePts()
x1,x2,F=simul.getDataOut()
print(F)


structOut["space"]["sampling"]["init_size"]=200
simul=batmanIO('',structOut)
simul.run()
simul.read()
X=simul.getSpacePts()
x1,x2,F=simul.getDataOut()
print(F)



# for i in range(len(F)):
#     plt.plot(X,F[i],label='x1='+str(x1[i])+' x2='+str(x2[i]))
# plt.legend()
# plotInfo(plt,pred.getParamInText())
# plt.xlabel("X")
# plt.ylabel("h")
# plt.savefig("plot/"+strftime("%Y-%m-%d %H:%M:%S", gmtime())+".png")
# plt.show()