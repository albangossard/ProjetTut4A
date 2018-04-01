from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

list_init_size=[5,10,15,20,50]
list_Q2=[]

# structOut["surrogate"]["method"]="kriging"
structOut["surrogate"]["strategy"]="LS"

for init_size in list_init_size:
    structOut["space"]["sampling"]["init_size"]=init_size
    print("Simul for init_size="+str(init_size))
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    Q2=simul.getQ2()
    list_Q2.append(Q2)
    print("Q2="+str(Q2))
    X=simul.getSpacePts()
    x1,x2,F=simul.getDataOut(0)
    plt.plot(X,F,label='init_size='+str(init_size))
list_init_size=np.array(list_init_size)
list_Q2=np.array(list_Q2)
plt.legend()
# plotInfo(plt,simul.getParamInText())
plt.xlabel("Abscisse X (m)")
plt.ylabel("Water level h (m)")
plt.title("Water level along the abscisse")
fileName=os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())
plt.savefig("plot/"+fileName+".png",dpi=500)
simul.saveSettings("plot/"+fileName+".json")
np.savetxt("plot/"+fileName+"_list_init_size.dat", list_init_size)
np.savetxt("plot/"+fileName+"_list_Q2.dat", list_Q2)
plt.show()

plt.plot(list_init_size, list_Q2)
plt.show()
