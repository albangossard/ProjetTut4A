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

list_gamme=[0,1,2]
list_choice=[0,1,2]
# list_choice=[1]

if method=='pc':
    degree = degree_default

for choice in list_choice:

    ## Custom response surface
    fig, ax = plt.subplots()

    ax.plot(np.linspace(corner_default[0][0],corner_default[1][0],5), seuil_Q_1*np.ones(5), linestyle=':', color='black', linewidth=1)
    ax.plot(np.linspace(corner_default[0][0],corner_default[1][0],5), seuil_Q_2*np.ones(5), linestyle=':', color='black', linewidth=1)

    list_h_pred=[]
    list_h_val=[]
    list_err=[]
    list_ks_tot = []
    list_q_tot = []

    for gamme in list_gamme:
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
        print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
        print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))


        x_train,y_train=parser2(list_ks,list_q,list_h)
        if gamme==-1:
            S=Substitut('sensAnalysis/sensAnalysis_'+distribName+'_choice='+str(choice),x_train,y_train,corners=corners, dists=dists, dists_UQ=dists_UQ)
        else:
            S=Substitut('sensAnalysis/sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice),x_train,y_train,corners=corners, dists=dists, dists_UQ=dists_UQ)


        list_ks = np.array(list_ks)
        list_q = np.array(list_q)
        list_h = np.array(list_h)


        ##############################
        for i,(ks,q,h) in enumerate(zip(list_ks,list_q,list_h)):
            if type(list_ks).__module__ == np.__name__:
                list_ks_tmp=list_ks[:].tolist()
                list_q_tmp=list_q[:].tolist()
                list_h_tmp=list_h[:].tolist()
            else:
                list_ks_tmp=list_ks[:]
                list_q_tmp=list_q[:]
                list_h_tmp=list_h[:]
            ks=float(list_ks_tmp.pop(i))
            q=float(list_q_tmp.pop(i))
            h=float(list_h_tmp.pop(i))
            x_train,y_train=parser2(list_ks_tmp,list_q_tmp,list_h_tmp)
            x_test=[[ks,q]]

            if gamme==-1:
                S=Substitut('sensAnalysis/sensAnalysis_'+distribName+'_choice='+str(choice),x_train,y_train,corners=corners, dists=dists, dists_UQ=dists_UQ)
            else:
                S=Substitut('sensAnalysis/sensAnalysis_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice),x_train,y_train,corners=corners, dists=dists, dists_UQ=dists_UQ)
            
            if method=='krig':
                S.buildK()
                y_pred=S.predictK(x_test)[0,0]
            else:
                S.buildPC(degree)
                y_pred=S.predictPC(x_test)[0,0]
            list_h_pred.append(y_pred)
            list_h_val.append(h)
            err=np.abs((y_pred-h)/h)
            list_err.append(err)
            list_ks_tot.append(ks)
            list_q_tot.append(q)
        ##############################

    ratio_plot=maxSizeScatter/np.max(list_err)
    for i,(ks,q,h,err) in enumerate(zip(list_ks_tot,list_q_tot,list_h_val,list_err)):
        p = ax.scatter(ks, q, c=h, s=err*ratio_plot, cmap=plt.cm.autumn, vmin=np.min(list_h_val), vmax=np.max(list_h_val))
        ax.annotate(str(np.round(err,4)), (ks, q), fontsize=6)
    cb = fig.colorbar(p)
    plt.xlabel('Ks')
    plt.ylabel('Q')
    plt.title('h')

    if method=='krig':
        plt.savefig('sensAnalysis/sensAnalysis_'+distribName+'_choice='+str(choice)+'/LOO_resp_surface_one_plot_krig.png',dpi=dpi_plot)
    if method=='pc':
        plt.savefig('sensAnalysis/sensAnalysis_'+distribName+'_choice='+str(choice)+'/LOO_resp_surface_one_plot_pc.png',dpi=dpi_plot)
    plt.clf()