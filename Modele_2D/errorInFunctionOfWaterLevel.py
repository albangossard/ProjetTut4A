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
gamme=-1

if distribName=='pc':
    degree = 6

for choice in list_choice:
    if gamme==-1:
        if distribName=='pc':
            list_h_pred_krig = np.loadtxt('postProcessingData/LOO_list_h_pred_'+method+'_degree='+str(degree)+'_'+distribName+'_choice='+str(choice)+'.txt')
            list_h_val_krig = np.loadtxt('postProcessingData/LOO_list_h_val_'+method+'_degree='+str(degree)+'_'+distribName+'_choice='+str(choice)+'.txt')
        else:
            list_h_pred_krig = np.loadtxt('postProcessingData/LOO_list_h_pred_'+method+'_'+distribName+'_choice='+str(choice)+'.txt')
            list_h_val_krig = np.loadtxt('postProcessingData/LOO_list_h_val_'+method+'_'+distribName+'_choice='+str(choice)+'.txt')
    else:
        if distribName=='pc':
            list_h_pred_krig = np.loadtxt('postProcessingData/LOO_list_h_pred_'+method+'_degree='+str(degree)+'_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'.txt')
            list_h_val_krig = np.loadtxt('postProcessingData/LOO_list_h_val_'+method+'_degree='+str(degree)+'_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'.txt')
        else:
            list_h_pred_krig = np.loadtxt('postProcessingData/LOO_list_h_pred_'+method+'_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'.txt')
            list_h_val_krig = np.loadtxt('postProcessingData/LOO_list_h_val_'+method+'_'+distribName+'_gamme='+str(gamme)+'_choice='+str(choice)+'.txt')
    err = np.abs(list_h_val_krig-list_h_pred_krig)
    plt.scatter(list_h_val_krig, err)
    plt.show()
    # plt.clf()