from Analyse import *
import matplotlib
# matplotlib.pyplot.switch_backend('agg')
import matplotlib.pyplot as plt

fname='init_size_RAPPORT'

list_init_size=np.loadtxt(fname+'/'+"init_size.dat")
list_q2K=np.loadtxt(fname+'/'+"Q2K.dat")
list_q2PC=np.loadtxt(fname+'/'+"q2PC.dat")
list_mseK=np.loadtxt(fname+'/'+"mseK.dat")
list_msePC=np.loadtxt(fname+'/'+"msePC.dat")

plt.semilogy(list_init_size,list_msePC,label='PC')
plt.semilogy(list_init_size,list_mseK,label='Kriging')
plt.xlabel('init_size')
plt.ylabel('mse')
plt.legend()
plt.tight_layout()
plt.savefig(fname+'/'+fname+'_mse.png',dpi=300)
plt.show()

plt.plot(list_init_size,list_q2PC,label='PC')
plt.plot(list_init_size,list_q2K,label='Kriging')
plt.xlabel('init_size')
plt.ylabel('q2')
plt.legend()
plt.tight_layout()
plt.savefig(fname+'/'+fname+'_q2.png',dpi=300)
plt.show()
