from Analyse import *
import matplotlib.pyplot as plt

fname='init_size3'
degree=10*0+5
# list_init_size=[180,200,250,300]
list_init_size=[50,70,100,130,150,180,200,250,300]

list_msePC=[]
list_q2PC=[]
list_mseK=[]
list_q2K=[]
for i,init_size in enumerate(list_init_size):
    A=Analyse(fname+'/'+str(init_size),init_size=init_size)
    A.test()
    
    A.surrogateKriging()
    mseKriging,q2Kriging=A.getSensibilityKriging()
    print(">>> Kriging mse="+str(mseKriging)+" q2="+str(q2Kriging))
    list_mseK.append(mseKriging)
    list_q2K.append(q2Kriging)
    
    A.surrogatePC(degree=degree)
    msePC,q2PC=A.getSensibilityPC()
    print(">>> PC init_size="+str(init_size)+" mse="+str(msePC)+" q2="+str(q2PC))
    list_msePC.append(msePC)
    list_q2PC.append(q2PC)
fig, ax1 = plt.subplots()
ax1.semilogy(list_init_size,list_msePC,'b',label='PC')
ax1.semilogy(list_init_size,list_mseK,'b.',label='Kriging')
ax1.set_xlabel('init_size')
ax1.set_ylabel('mse', color='b')
ax1.tick_params('y', colors='b')
ax2 = ax1.twinx()
ax2.semilogy(list_init_size,list_q2PC,'r',label='PC')
ax2.semilogy(list_init_size,list_q2K,'r.',label='Kriging')
ax2.set_ylabel('q2', color='r')
ax2.tick_params('y', colors='r')
plt.legend()
fig.tight_layout()
plt.savefig(fname+'/'+fname+'.png',dpi=300)
np.savetxt(fname+'/'+"init_size.dat", list_init_size)
np.savetxt(fname+'/'+"Q2K.dat", list_q2K)
np.savetxt(fname+'/'+"q2PC.dat", list_q2PC)
np.savetxt(fname+'/'+"mseK.dat", list_mseK)
np.savetxt(fname+'/'+"msePC.dat", list_msePC)
plt.show()
