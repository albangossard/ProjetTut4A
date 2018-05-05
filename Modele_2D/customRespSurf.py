import sys
import matplotlib
matplotlib.use('Agg')
from Substitut import *

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
list_gamme=[-1,0,1,2]
seuil_Q_1=3000.
seuil_Q_2=6000.

for gamme in list_gamme:

    for choice in list_choice:
        if gamme==-1:
            list_ks, list_q, list_h = reader('data2.txt', choice)
            corners=([17.,1600.],[45.,9900.])
            a=1600.
            b=9900.
            if distribName=='Norm':
                mu=(a+b)/2.
                sigma=(b-mu)/2.
                dists_UQ=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
                dists=[ot.Uniform(17., 45.), ot.Normal(mu, sigma)]
            else:
                dists_UQ=['Uniform(17., 45.)','Uniform('+str(a)+', '+str(b)+')']
                dists=[ot.Uniform(17., 45.), ot.Uniform(a, b)]
        else:
            data_gamme=np.load('gamme_choice='+str(choice)+'.npy')
            id_gamme=gamme
            gamme=data_gamme[id_gamme]
            list_ks=gamme[0]
            list_q=gamme[1]
            list_h=gamme[2]
            gamme=id_gamme
            """if id_gamme==0:
                corners=([17.,1600.],[45.,seuil_Q_1])
            elif id_gamme==1:
                corners=([17.,seuil_Q_1],[45.,seuil_Q_2])
            else:
                corners=([17.,seuil_Q_2],[45.,9900.])"""
            if id_gamme==0:
                corners=([17.,1600.],[45.,seuil_Q_1])
                a=1600.
                b=seuil_Q_1
                if distribName=='Norm':
                    mu=(a+b)/2.
                    sigma=(b-mu)/2.
                    dists_UQ=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
                    dists=[ot.Uniform(17., 45.), ot.Normal(mu, sigma)]
                else:
                    dists_UQ=['Uniform(17., 45.)','Uniform('+str(a)+', '+str(b)+')']
                    dists=[ot.Uniform(17., 45.), ot.Uniform(a, b)]
            elif id_gamme==1:
                corners=([17.,seuil_Q_1],[45.,seuil_Q_2])
                a=seuil_Q_1
                b=seuil_Q_2
                if distribName=='Norm':
                    mu=(a+b)/2.
                    sigma=(b-mu)/2.
                    dists_UQ=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
                    dists=[ot.Uniform(17., 45.), ot.Normal(mu, sigma)]
                else:
                    dists_UQ=['Uniform(17., 45.)','Uniform('+str(a)+', '+str(b)+')']
                    dists=[ot.Uniform(17., 45.), ot.Uniform(a, b)]
            else:
                corners=([17.,seuil_Q_2],[45.,9900.])
                a=seuil_Q_2
                b=9900.
                if distribName=='Norm':
                    mu=(a+b)/2.
                    sigma=(b-mu)/2.
                    dists_UQ=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
                    dists=[ot.Uniform(17., 45.), ot.Normal(mu, sigma)]
                else:
                    dists_UQ=['Uniform(17., 45.)','Uniform('+str(a)+', '+str(b)+')']
                    dists=[ot.Uniform(17., 45.), ot.Uniform(a, b)]
        ################ TEST ################
        corners=([17.,1600.],[45.,9900.])
        a=1600.
        b=9900.
        mu=(a+b)/2.
        sigma=(b-mu)/2.
        # dists_UQ=['Uniform(17., 45.)','Normal('+str(mu)+', '+str(sigma)+')']
        dists=[ot.Uniform(17., 45.), ot.Normal(mu, sigma)]
        ######################################
        print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
        print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))


        x_train,y_train=parser2(list_ks,list_q,list_h)
        if gamme==-1:
            S=Substitut('sensAnalysis_'+distribName+'_choice='+str(choice),x_train,y_train,corners=corners, dists=dists, dists_UQ=dists_UQ)
        else:
            S=Substitut('sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice),x_train,y_train,corners=corners, dists=dists, dists_UQ=dists_UQ)




        if method=='krig':
            S.buildK()
            S.analysisK()


            ## Custom response surface for K
            nPtsRespSurf = 50*0+20
            listKsRS = np.linspace(corners[0][0], corners[1][0], nPtsRespSurf)
            listQRS = np.linspace(corners[0][1], corners[1][1], nPtsRespSurf)
            LKs, LQ = np.meshgrid(listKsRS, listQRS)
            hRS = LKs*0.
            for i, Ks in enumerate(listKsRS):
                for j, Q in enumerate(listQRS):
                    x_test = [[Ks, Q]]
                    hRS[j,i] = S.predictK(x_test)[0,0]


            fig, ax = plt.subplots()

            p = ax.pcolor(listKsRS, listQRS, hRS, cmap=plt.cm.Blues, vmin=np.min(hRS), vmax=np.max(hRS))
            for ks,q,h in zip(np.array(list_ks).astype(np.float), np.array(list_q).astype(np.float), list_h):
                ax.scatter(ks, q, c=h, cmap=plt.cm.Blues, vmin=np.min(hRS), vmax=np.max(hRS))
            cb = fig.colorbar(p)
            plt.xlabel('Ks')
            plt.ylabel('Q')
            plt.title('h')

            if gamme==-1:
                plt.savefig('sensAnalysis_'+distribName+'_choice='+str(choice)+'/custom_resp_surface_krig.png',dpi=200)
            else:
                plt.savefig('sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'/custom_resp_surface_krig.png',dpi=200)
            plt.clf()



        if method=='pc':
            S.buildPC()
            S.analysisPC()


            ## Custom response surface for PC
            nPtsRespSurf = 50*0+20
            listKsRS = np.linspace(corners[0][0], corners[1][0], nPtsRespSurf)
            listQRS = np.linspace(corners[0][1], corners[1][1], nPtsRespSurf)
            LKs, LQ = np.meshgrid(listKsRS, listQRS)
            hRS = LKs*0.
            for i, Ks in enumerate(listKsRS):
                for j, Q in enumerate(listQRS):
                    x_test = [[Ks, Q]]
                    hRS[j,i] = S.predictPC(x_test)[0,0]


            fig, ax = plt.subplots()

            p = ax.pcolor(listKsRS, listQRS, hRS, cmap=plt.cm.Blues, vmin=np.min(hRS), vmax=np.max(hRS))
            for ks,q,h in zip(np.array(list_ks).astype(np.float), np.array(list_q).astype(np.float), list_h):
                ax.scatter(ks, q, c=h, cmap=plt.cm.Blues, vmin=np.min(hRS), vmax=np.max(hRS))
            cb = fig.colorbar(p)
            plt.xlabel('Ks')
            plt.ylabel('Q')
            plt.title('h')

            if gamme==-1:
                plt.savefig('sensAnalysis_'+distribName+'_choice='+str(choice)+'/custom_resp_surface_pc.png',dpi=200)
            else:
                plt.savefig('sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'/custom_resp_surface_pc.png',dpi=200)
            plt.clf()