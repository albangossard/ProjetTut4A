from config import *
import scipy.stats as scs

choice=0
list_ks, list_q, list_h = reader('data2.txt', choice)
list_ks=np.array(list_ks).astype(np.float)
list_q=np.array(list_q).astype(np.float)
list_h=np.array(list_h).astype(np.float)

fig, ax = plt.subplots()

for ks,q,h in zip(list_ks, list_q, list_h):
    ax.scatter(ks, q, c='black')
plt.xlabel('Ks')
plt.ylabel('Q')
plt.savefig("doe/mapping.png", dpi=dpi_plot)
plt.show()

plt.hist(list_ks,bins=20)
plt.xlabel('Ks')
plt.ylabel('Frequency')
plt.savefig("doe/distrib_ks.png", dpi=dpi_plot)
plt.show()

# plt.hist(list_q,bins=10,orientation='horizontal')
plt.hist(list_q,bins=20)
plt.xlabel('Q')
plt.ylabel('Frequency')
plt.savefig("doe/distrib_q.png", dpi=dpi_plot)
plt.show()