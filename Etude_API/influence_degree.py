from Analyse import *
import matplotlib.pyplot as plt

fname='degree'
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
fig, ax1 = plt.subplots()
ax1.semilogy(list_degree,list_msePC,'b',label='PC')
ax1.semilogy(np.linspace(list_degree[0],list_degree[-1],50),np.linspace(mseKriging,mseKriging,50),'b.',label='Kriging')
ax1.set_xlabel('degree')
ax1.set_ylabel('mse', color='b')
ax1.tick_params('y', colors='b')
ax2 = ax1.twinx()
ax2.semilogy(list_degree,list_q2PC,'r',label='PC')
ax2.semilogy(np.linspace(list_degree[0],list_degree[-1],50),np.linspace(q2Kriging,q2Kriging,50),'r.',label='Kriging')
ax2.set_ylabel('q2', color='r')
ax2.tick_params('y', colors='r')
plt.legend()
fig.tight_layout()
plt.savefig(fname+'/'+fname+'.png',dpi=300)
plt.show()
