from Substitut import *

list_choice=[0,1,2]
gamme=-1
seuil_Q_1=3000.
seuil_Q_2=6000.
dists=['Uniform(17., 45.)','Normal(5750., 2075.)']; distribName='Norm'
# dists=['Uniform(17., 45.)','Uniform(1600., 9900.)']; distribName='Unif'

for choice in list_choice:
    if gamme==-1:
        list_h_pred_krig = np.loadtxt('postProcessingData/LOO_list_h_pred_krig_'+distribName+'_choice='+str(choice)+'.txt')
        list_h_val_krig = np.loadtxt('postProcessingData/LOO_list_h_val_krig_'+distribName+'_choice='+str(choice)+'.txt')
    else:
        list_h_pred_krig = np.loadtxt('postProcessingData/LOO_list_h_pred_krig_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'.txt')
        list_h_val_krig = np.loadtxt('postProcessingData/LOO_list_h_val_krig_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'.txt')
    err = np.abs(list_h_val_krig-list_h_pred_krig)
    plt.scatter(list_h_val_krig, err)
    plt.show()
