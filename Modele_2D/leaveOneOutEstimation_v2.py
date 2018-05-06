from config import *

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

if method=='pc':
    degree = 6

if distribName=='Norm':
    dists=[ot.Uniform(17., 45.), ot.Normal(5750., 2075.)]
else:
    dists=[ot.Uniform(17., 45.), ot.Uniform(1600., 9900.)]

for choice in list_choice:
    print("\n{:#^70s}".format("choice="+str(choice)))
    list_ks, list_q, list_h = reader('data2.txt', choice)
    print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
    print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))


    corners=([17.,1600.],[45.,9900.])

    err=0.
    list_h_pred=[]
    list_h_val=[]
    for i,(ks,q,h) in enumerate(zip(list_ks,list_q,list_h)):
        list_ks_tmp=list_ks[:]
        list_q_tmp=list_q[:]
        list_h_tmp=list_h[:]
        ks=float(list_ks_tmp.pop(i))
        q=float(list_q_tmp.pop(i))
        h=float(list_h_tmp.pop(i))
        x_train,y_train=parser2(list_ks_tmp,list_q_tmp,list_h_tmp)
        x_test=[[ks,q]]

        S=Substitut('test',x_train,y_train,corners=corners,verbose=0, dists=dists)
        if method=='krig':
            S.buildK()
            y_pred=S.predictK(x_test)[0,0]
        else:
            S.buildPC(degree)
            y_pred=S.predictPC(x_test)[0,0]
        list_h_pred.append(y_pred)
        list_h_val.append(h)
        print("y_pred="+str(y_pred)+"\t h="+str(h)+"\t err(%)="+str((y_pred-h)/h))
        err+=(y_pred-h)**2.
    list_h_pred=np.array(list_h_pred)
    list_h_val=np.array(list_h_val)
    err/=len(list_h_val)
    print("err="+str(err))
    if method=='pc':
        np.savetxt('postProcessingData/LOO_list_h_pred_'+method+'_degree='+str(degree)+'_'+distribName+'_choice='+str(choice)+'.txt', list_h_pred)
        np.savetxt('postProcessingData/LOO_list_h_val_'+method+'_degree='+str(degree)+'_'+distribName+'_choice='+str(choice)+'.txt', list_h_val)
    else:
        np.savetxt('postProcessingData/LOO_list_h_pred_'+method+'_'+distribName+'_choice='+str(choice)+'.txt', list_h_pred)
        np.savetxt('postProcessingData/LOO_list_h_val_'+method+'_'+distribName+'_choice='+str(choice)+'.txt', list_h_val)
    errNorm=1.-len(list_h_val)*err/(np.sum((list_h_val-np.mean(list_h_val))**2.))
    print("errNorm="+str(errNorm)+" \t=\t "+str(1.-errNorm))

    q2_loo = r2_score(list_h_val, list_h_pred)
    print("q2_loo="+str(q2_loo))
    if method=='pc':
        np.savetxt('postProcessingData/LOO_q2_loo_'+method+'_degree='+str(degree)+'_'+distribName+'_choice='+str(choice)+'.txt', [q2_loo])
    else:
        np.savetxt('postProcessingData/LOO_q2_loo_'+method+'_'+distribName+'_choice='+str(choice)+'.txt', [q2_loo])
