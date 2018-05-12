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
    degree = degree_default

if distribName=='Norm':
    dists=[ot.Uniform(17., 45.), ot.Normal(5750., 2075.)]
else:
    dists=[ot.Uniform(17., 45.), ot.Uniform(1600., 9900.)]

for choice in list_choice:
    print("\n{:#^70s}".format("choice="+str(choice)))
    list_ks, list_q, list_h = reader('data2.txt', choice)
    print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
    print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))

    corners = corner_default

    x_train,y_train=parser2(list_ks,list_q,list_h)
    S=Substitut('test',x_train,y_train,corners=corners,verbose=0, dists=dists)
    if method=='krig':
        S.buildK()
        q2_loo=S.k_predictor.estimate_quality()[0]
    else:
        S.buildPC(degree)
        q2_loo=S.pc_predictor.estimate_quality()[0]
    
    print("q2_loo="+str(q2_loo))
    if method=='pc':
        np.savetxt('postProcessingData/LOO_q2_loo_'+method+'_degree='+str(degree)+'_'+distribName+'_choice='+str(choice)+'.txt', [q2_loo])
    else:
        np.savetxt('postProcessingData/LOO_q2_loo_'+method+'_'+distribName+'_choice='+str(choice)+'.txt', [q2_loo])
