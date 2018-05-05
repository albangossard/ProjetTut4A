import sys
from Substitut import *
from sklearn.metrics import r2_score

options = [sys.argv[i+1] for i in range(len(sys.argv)-1)]

if 'k' in options:
    method = 'krig'
if 'pc' in options:
    method = 'pc'
if 'N' in options:
    distribName = 'Norm'
if 'U' in options:
    distribName = 'Unif'

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
            a=1600.
            b=seuil_Q_1
            if distribName=='Norm':
                mu=(a+b)/2.
                sigma=(b-mu)/2.
                dists=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
            else:
                dists=['Uniform(17., 45.)','Uniform('+str(a)+', '+str(b)+')']
        elif id_gamme==1:
            corners=([17.,seuil_Q_1],[45.,seuil_Q_2])
            a=seuil_Q_1
            b=seuil_Q_2
            if distribName=='Norm':
                mu=(a+b)/2.
                sigma=(b-mu)/2.
                dists=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
            else:
                dists=['Uniform(17., 45.)','Uniform('+str(a)+', '+str(b)+')']
        else:
            corners=([17.,seuil_Q_2],[45.,9900.])
            a=seuil_Q_2
            b=9900.
            if distribName=='Norm':
                mu=(a+b)/2.
                sigma=(b-mu)/2.
                dists=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
            else:
                dists=['Uniform(17., 45.)','Uniform('+str(a)+', '+str(b)+')']
        ################ TEST ################
        corners=([17.,1600.],[45.,9900.])
        a=1600.
        b=9900.
        mu=(a+b)/2.
        sigma=(b-mu)/2.
        dists=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
        ######################################
        print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
        print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))
        
        err=0.
        list_h_pred_krig=[]
        list_h_val_krig=[]
        for i,(ks,q,h) in enumerate(zip(list_ks,list_q,list_h)):
            list_ks_tmp=list_ks[:].tolist()
            list_q_tmp=list_q[:].tolist()
            list_h_tmp=list_h[:].tolist()
            ks=float(list_ks_tmp.pop(i))
            q=float(list_q_tmp.pop(i))
            h=float(list_h_tmp.pop(i))
            x_train,y_train=parser2(list_ks_tmp,list_q_tmp,list_h_tmp)
            x_test=[[ks,q]]

            # print("ks="+str(ks)+"\t q="+str(q))
            S=Substitut('test',x_train,y_train,corners=corners,verbose=0, dists=dists)
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
        np.savetxt('postProcessingData/LOO_list_h_pred_'+method+'_'+distribName+'_gamme='+str(id_gamme)+'_choice='+str(choice)+'.txt', list_h_pred_krig)
        np.savetxt('postProcessingData/LOO_list_h_val_'+method+'_'+distribName+'_gamme='+str(id_gamme)+'_choice='+str(choice)+'.txt', list_h_val_krig)
        errNorm=1.-len(list_h_val_krig)*err/(np.sum((list_h_val_krig-np.mean(list_h_val_krig))**2.))
        print("errNorm="+str(errNorm)+" \t=\t "+str(1.-errNorm))

        q2_loo = r2_score(list_h_val_krig, list_h_pred_krig)
        print("q2_loo="+str(q2_loo))
        np.savetxt('postProcessingData/LOO_q2_loo_'+method+'_'+distribName+'_gamme='+str(id_gamme)+'_choice='+str(choice)+'.txt', [q2_loo])
