from batmanIO import *
import matplotlib.pyplot as plt
from time import gmtime, strftime

list_degree=[1,2,3,4,5]
list_Q2=[]

# structOut["surrogate"]["method"]="kriging"
structOut["surrogate"]["strategy"]="Quad"

for degree in list_degree:
    structOut["surrogate"]["degree"]=degree
    print("Simul for degree="+str(degree))
    simul=batmanIO('',structOut)
    simul.run()
    simul.read()
    Q2=simul.getQ2()
    list_Q2.append(Q2)
    print("Q2="+str(Q2))
    # X=simul.getSpacePts()
    x1,x2,x3,F=simul.getDataOut(0)
    # plt.plot(X,F,label='degree='+str(degree))
list_degree=np.array(list_degree)
list_Q2=np.array(list_Q2)
# plt.legend()
# plotInfo(plt,simul.getParamInText())
# plt.xlabel("Abscisse X (m)")
# plt.ylabel("Water level h (m)")
# plt.title("Water level along the abscisse")
fileName=os.path.basename(__file__)+"_"+strftime("%Y-%m-%d %H:%M:%S", gmtime())
# plt.savefig("plot/"+fileName+".png",dpi=500)
simul.saveSettings("plot/"+fileName+".json")
np.savetxt("plot/"+fileName+"_list_degree.dat", list_degree)
np.savetxt("plot/"+fileName+"_list_Q2.dat", list_Q2)
# plt.show()

plt.plot(list_degree, list_Q2)
plt.show()
