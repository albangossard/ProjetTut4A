from Substitut import *

# choice=0
list_choice=[0,1,2]
gamme=-1*0+2
seuil_Q_1=3000.
seuil_Q_2=6000.

for choice in list_choice:
    if gamme==-1:
        list_ks, list_q, list_h = reader('data2.txt', choice)
        corners=([17.,1600.],[45.,9900.])
    else:
        list_gamme=np.load('gamme_choice='+str(choice)+'.npy')
        id_gamme=gamme
        gamme=list_gamme[id_gamme]
        list_ks=gamme[0]
        list_q=gamme[1]
        list_h=gamme[2]
        gamme=id_gamme
        if id_gamme==0:
            corners=([17.,1600.],[45.,seuil_Q_1])
        elif id_gamme==1:
            corners=([17.,seuil_Q_1],[45.,seuil_Q_2])
        else:
            corners=([17.,seuil_Q_2],[45.,9900.])
    print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
    print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))


    x_train,y_train=parser2(list_ks,list_q,list_h)
    if gamme==-1:
        S=Substitut('sensAnalysis_choice='+str(choice),x_train,y_train,corners=corners)
    else:
        S=Substitut('sensAnalysis_gamme='+str(gamme)+'_choice='+str(choice),x_train,y_train,corners=corners)
    S.buildK()
    S.analysisK()




    ## Custom response surface
    nPtsRespSurf = 50*0+20
    listKsRS = np.linspace(corners[0][0], corners[1][0], nPtsRespSurf)
    listQRS = np.linspace(corners[0][1], corners[1][1], nPtsRespSurf)
    LKs, LQ = np.meshgrid(listKsRS, listQRS)
    hRS = LKs*0.
    for i, Ks in enumerate(listKsRS):
        for j, Q in enumerate(listQRS):
            x_test = [[Ks, Q]]
            hRS[j,i] = S.predictK(x_test)[0,0]



    # list_h_pred = np.loadtxt('LOO_list_h_pred_krig_choice='+str(choice)+'.txt')
    # err, list_err = estimateLOOError(list_ks, list_q, list_h, list_h_pred)
    # print("err="+str(err))



    fig, ax = plt.subplots()

    p = ax.pcolor(listKsRS, listQRS, hRS, cmap=plt.cm.Blues, vmin=np.min(hRS), vmax=np.max(hRS))
    for ks,q,h in zip(np.array(list_ks).astype(np.float), np.array(list_q).astype(np.float), list_h):
        ax.scatter(ks, q, c=h, cmap=plt.cm.Blues, vmin=np.min(hRS), vmax=np.max(hRS))
    cb = fig.colorbar(p)
    plt.xlabel('Ks')
    plt.ylabel('Q')
    plt.title('h')

    if gamme==-1:
        plt.savefig('sensAnalysis_choice='+str(choice)+'/custom_resp_surface_krig0.png',dpi=200)
    else:
        plt.savefig('sensAnalysis_gamme='+str(gamme)+'_choice='+str(choice)+'/custom_resp_surface_krig0.png',dpi=200)
    # plt.show()
