from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

init_size=15
list_distrib=[["Uniform(15., 60.)", "Uniform(2500., 6000.)"],
                ["Uniform(15., 60.)", "BetaMuSigma(4035, 400, 2500, 6000).getDistribution()"],
                ["BetaMuSigma(37.5, 5., 15., 60.).getDistribution()", "Uniform(2500., 6000.)"],
                ["BetaMuSigma(37.5, 5., 15., 60.).getDistribution()", "BetaMuSigma(4035, 400, 2500, 6000).getDistribution()"]
                ]
init_size_ref=200
#distrib_ref=["BetaMuSigma(37.5, 5., 15., 60.).getDistribution()", "BetaMuSigma(4035, 400, 2500, 6000).getDistribution()"]
list_Q2=[]

structOut["surrogate"]["strategy"]="LS"

# structOut["space"]["sampling"]["init_size"]=init_size_ref
# structOut["space"]["sampling"]["distributions"]=distrib_ref
# simul=batmanIO('',structOut)
# simul.run()
# simul.read()
# X=simul.getSpacePts()
# x1,x2,F=simul.getDataOut(0)
# plt.plot(X,F,label='init_size='+str(init_size_ref)+' distrib=Dref')

structOut["space"]["sampling"]["init_size"]=init_size
for i,distrib in enumerate(list_distrib):
    structOut["space"]["sampling"]["distributions"]=distrib
    print("Simul for distrib="+str(distrib))
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    Q2=simul.getQ2()
    list_Q2.append(Q2)
    print("Q2="+str(Q2))
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='init_size='+str(init_size)+' distrib=D'+str(i))
list_distrib=np.array(list_distrib)
list_Q2=np.array(list_Q2)
plt.legend()
# plotInfo(plt,simul.getParamInText())
plt.xlabel("Abscisse X (m)")
plt.ylabel("Water level h (m)")
plt.title("Water level along the abscisse")
fileName=os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())
plt.savefig("plot/"+fileName+".png",dpi=500)
simul.saveSettings("plot/"+fileName+".json")
np.savetxt("plot/"+fileName+"_list_distrib.dat", list_distrib)
np.savetxt("plot/"+fileName+"_list_Q2.dat", list_Q2)
plt.show()

# plt.plot(list_distrib, list_Q2)
# plt.show()
