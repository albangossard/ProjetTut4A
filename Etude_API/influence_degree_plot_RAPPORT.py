from Analyse import *
import matplotlib
# matplotlib.pyplot.switch_backend('agg')
import matplotlib.pyplot as plt

fname='degree_RAPPORT'

list_degree=np.loadtxt(fname+'/'+"degree.dat")
q2Kriging=np.loadtxt(fname+'/'+"Q2K.dat")
list_q2PC=np.loadtxt(fname+'/'+"q2PC.dat")
mseKriging=np.loadtxt(fname+'/'+"mseK.dat")
list_msePC=np.loadtxt(fname+'/'+"msePC.dat")




fig, ax1 = plt.subplots()
ax1.semilogy(list_degree,list_msePC,'b',label='PC')
ax1.semilogy(np.linspace(list_degree[0],list_degree[-1],50),np.linspace(mseKriging,mseKriging,50),'b.',label='Kriging')
ax1.set_xlabel('degree')
ax1.set_ylabel('mse', color='b')
ax1.tick_params('y', colors='b')
ax2 = ax1.twinx()
# ax2.semilogy(list_degree,list_q2PC,'r',label='PC')
ax2.plot(list_degree,list_q2PC,'r',label='PC')
# ax2.semilogy(np.linspace(list_degree[0],list_degree[-1],50),np.linspace(q2Kriging,q2Kriging,50),'r.',label='Kriging')
ax2.plot(np.linspace(list_degree[0],list_degree[-1],50),np.linspace(q2Kriging,q2Kriging,50),'r.',label='Kriging')
ax2.set_ylabel('q2', color='r')
ax2.tick_params('y', colors='r')
plt.legend()
fig.tight_layout()
plt.savefig(fname+'/'+fname+'.png',dpi=300)
plt.show()
