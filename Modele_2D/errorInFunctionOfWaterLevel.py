import sys
import matplotlib
matplotlib.use('Qt5Agg')
# print(matplotlib.get_backend())
from Substitut import *

options = [sys.argv[i+1] for i in range(len(sys.argv)-1)]

if 'k' in options:
    method = 'krig'
if 'pc' in options:
    method = 'pc'

list_choice=[0,1,2]
gamme=-1
distribName='Norm'
# distribName='Unif'

for choice in list_choice:
    if gamme==-1:
        list_h_pred_krig = np.loadtxt('postProcessingData/LOO_list_h_pred_'+method+'_'+distribName+'_choice='+str(choice)+'.txt')
        list_h_val_krig = np.loadtxt('postProcessingData/LOO_list_h_val_'+method+'_'+distribName+'_choice='+str(choice)+'.txt')
    else:
        list_h_pred_krig = np.loadtxt('postProcessingData/LOO_list_h_pred_'+method+'_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'.txt')
        list_h_val_krig = np.loadtxt('postProcessingData/LOO_list_h_val_'+method+'_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'.txt')
    err = np.abs(list_h_val_krig-list_h_pred_krig)
    plt.scatter(list_h_val_krig, err)
    plt.show()
