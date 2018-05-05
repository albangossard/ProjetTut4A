from Substitut import *
from sklearn.metrics import r2_score

list_choice=[0,1,2]
seuil_Q_1=3000.
seuil_Q_2=6000.

for choice in list_choice:
    #       ks q  h
    gamme=[[[],[],[]], # gamme 0
            [[],[],[]], # gamme 1
            [[],[],[]]] # gamme 2
    list_ks, list_q, list_h = reader('data2.txt', choice)
    list_ks=np.array(list_ks).astype(np.float)
    list_q=np.array(list_q).astype(np.float)
    list_h=np.array(list_h).astype(np.float)
    print(list_ks)
    print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
    print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))
    for i,(ks,q,h) in enumerate(zip(list_ks,list_q,list_h)):
        # if q<=seuil_Q_1:
        if True:
            gamme[0][0].append(ks)
            gamme[0][1].append(q)
            gamme[0][2].append(h)
        # elif q<=seuil_Q_2:
        if True:
            gamme[1][0].append(ks)
            gamme[1][1].append(q)
            gamme[1][2].append(h)
        # else:
        if True:
            gamme[2][0].append(ks)
            gamme[2][1].append(q)
            gamme[2][2].append(h)
    for i in range(3):
        for j in range(3):
            gamme[i][j]=np.array(gamme[i][j])
    np.save('gamme_choice='+str(choice)+'.npy', gamme)