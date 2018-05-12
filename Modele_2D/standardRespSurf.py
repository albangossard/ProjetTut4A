import matplotlib
matplotlib.use('Agg')
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
if 'global' in options:
    global_compare='_glob'
    list_gamme=[0,1,2]
else:
    global_compare=''
    list_gamme=[-1,0,1,2]

list_choice=[0,1,2]
# list_choice=[1]
# list_gamme=[-1]
# list_gamme=[-1,1]
list_gamme=[1]

if method=='pc':
    degree = degree_default

for gamme in list_gamme:

    for choice in list_choice:
        if gamme==-1:
            list_ks, list_q, list_h = reader('data2.txt', choice)
            corners = corner_default
            a=lower
            b=upper
        else:
            data_gamme=np.load('gamme_choice='+str(choice)+'.npy')
            id_gamme=gamme
            gamme=data_gamme[id_gamme]
            list_ks=gamme[0]
            list_q=gamme[1]
            list_h=gamme[2]
            gamme=id_gamme
            if id_gamme==0:
                corners = corner_gamme0
                a=1600.
                b=seuil_Q_1
            elif id_gamme==1:
                corners = corner_gamme1
                a=seuil_Q_1
                b=seuil_Q_2
            else:
                corners = corner_gamme2
                a=seuil_Q_2
                b=upper
        if distribName=='Norm':
            mu=(a+b)/2.
            sigma=(b-mu)/2.
            dists_UQ=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
            dists=[ot.Uniform(17., 45.), ot.Normal(mu, sigma)]
        else:
            dists_UQ=['Uniform(17., 45.)','Uniform('+str(a)+', '+str(b)+')']
            dists=[ot.Uniform(17., 45.), ot.Uniform(a, b)]
        ################ TEST ################
        if global_compare=='_glob':
            print(global_compare+' mode !!!')
            corners = corner_default
            a=lower
            b=upper
            mu=(a+b)/2.
            sigma=(b-mu)/2.
            # dists_UQ=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
            dists=[ot.Uniform(17., 45.), ot.Normal(mu, sigma)]
        # print(dists)
        # print(dists_UQ)
        # print(list_ks)
        # print(list_q)
        ######################################
        print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
        print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))


        x_train,y_train=parser2(list_ks,list_q,list_h)
        if gamme==-1:
            S=Substitut('sensAnalysis/sensAnalysis_'+distribName+global_compare+'_choice='+str(choice),x_train,y_train,corners=corners, dists=dists, dists_UQ=dists_UQ)
        else:
            S=Substitut('sensAnalysis/sensAnalysis_'+distribName+global_compare+'_gamme='+str(gamme)+'_choice='+str(choice),x_train,y_train,corners=corners, dists=dists, dists_UQ=dists_UQ)


        if method=='krig':
            S.buildK()
            S.analysisK()


        if method=='pc':
            S.buildPC(degree)
            S.analysisPC()
