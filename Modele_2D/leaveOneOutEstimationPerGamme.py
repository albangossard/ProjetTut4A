from Substitut import *
from sklearn.metrics import r2_score

list_choice=[0,1,2]
seuil_Q_1=3000.
seuil_Q_2=6000.

for choice in list_choice:
    print("\n{:#^70s}".format("choice="+str(choice)))
    list_gamme=np.load('gamme_choice='+str(choice)+'.npy')
    for id_gamme,gamme in enumerate(list_gamme):
        print("\n{:#^50s}".format("gamme="+str(id_gamme)))
        list_ks=gamme[0]
        list_q=gamme[1]
        list_h=gamme[2]
        if id_gamme==0:
            corners=([17.,1600.],[45.,seuil_Q_1])
        elif id_gamme==1:
            corners=([17.,seuil_Q_1],[45.,seuil_Q_2])
        else:
            corners=([17.,seuil_Q_2],[45.,9900.])
        print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
        print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))
        
        err=0.
        list_h_pred_krig=[]
        list_h_val_krig=[]
        for i,(ks,q,h) in enumerate(zip(list_ks,list_q,list_h)):
            list_ks_tmp=list_ks[:]
            list_q_tmp=list_q[:]
            list_h_tmp=list_h[:]
            ks=float(list_ks_tmp.pop(i))
            q=float(list_q_tmp.pop(i))
            h=float(list_h_tmp.pop(i))
            x_train,y_train=parser2(list_ks_tmp,list_q_tmp,list_h_tmp)
            x_test=[[ks,q]]

            # print("ks="+str(ks)+"\t q="+str(q))
            S=Substitut('test',x_train,y_train,corners=corners,verbose=0)
            S.buildK()
            y_pred_krig=S.predictK(x_test)[0,0]
            list_h_pred_krig.append(y_pred_krig)
            list_h_val_krig.append(h)
            print("y_pred_krig="+str(y_pred_krig)+"\t h="+str(h)+"\t err(%)="+str((y_pred_krig-h)/h))
            err+=(y_pred_krig-h)**2.

        list_h_pred_krig=np.array(list_h_pred_krig)
        list_h_val_krig=np.array(list_h_val_krig)
        err/=len(list_h_val_krig)
        print("err="+str(err))
        np.savetxt('LOO_list_h_pred_krig_gamme='+str(id_gamme)+'_choice='+str(choice)+'.txt', list_h_pred_krig)
        np.savetxt('LOO_list_h_val_krig_gamme='+str(id_gamme)+'_choice='+str(choice)+'.txt', list_h_val_krig)
        errNorm=1.-len(list_h_val_krig)*err/(np.sum((list_h_val_krig-np.mean(list_h_val_krig))**2.))
        print("errNorm="+str(errNorm)+" \t=\t "+str(1.-errNorm))

        q2_loo = r2_score(list_h_val_krig, list_h_pred_krig)
        print("q2_loo="+str(q2_loo))
        np.savetxt('LOO_q2_loo_gamme='+str(id_gamme)+'_choice='+str(choice)+'.txt', [q2_loo])
