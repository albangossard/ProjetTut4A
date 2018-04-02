from Analyse import *
import matplotlib
matplotlib.pyplot.switch_backend('agg')
import matplotlib.pyplot as plt

fname='degree_RAPPORT'
init_size=180
list_degree=[3,4,5,6,7,8,9,10]
# list_degree=[4,5]

list_msePC=[]
list_q2PC=[]
for i,degree in enumerate(list_degree):
    A=Analyse(fname+'/'+str(degree),init_size=init_size)
    A.test()
    if i==0:
        A.surrogateKriging()
        mseKriging,q2Kriging=A.getSensibilityKriging()
        print(">>> Kriging mse="+str(mseKriging)+" q2="+str(q2Kriging))
    A.surrogatePC(degree=degree)
    msePC,q2PC=A.getSensibilityPC()
    del A
    print(">>> PC degree="+str(degree)+" mse="+str(msePC)+" q2="+str(q2PC))
    list_msePC.append(msePC)
    list_q2PC.append(q2PC)

np.savetxt(fname+'/'+"degree.dat", list_degree)
np.savetxt(fname+'/'+"Q2K.dat", [q2Kriging])
np.savetxt(fname+'/'+"q2PC.dat", list_q2PC)
np.savetxt(fname+'/'+"mseK.dat", [mseKriging])
np.savetxt(fname+'/'+"msePC.dat", list_msePC)
