import os
import batman
import openturns as ot
import numpy as np
from batman.functions.analytical import Channel_Flow
from batman.space import (Space, dists_to_ot)
from batman.uq import UQ
from batman.visualization import Kiviat3D, HdrBoxplot, response_surface, Tree
from batman.surrogate import SurrogateModel
from batman.surrogate import PC
from sklearn.metrics import (r2_score, mean_squared_error)

ot.Log.Show(ot.Log.ERROR)

def parser(list_ks,list_q0,list_q1,list_h):
    x_train=[]
    y_train=[]
    for (ks,q0,q1,h) in zip(list_ks,list_q0,list_q1,list_h):
        x_train.append([float(ks),float(q0+q1)])
        y_train.append([float(h)])
    x_train=np.array(x_train)
    y_train=np.array(y_train)
    return x_train,y_train

class Substitut:
    def __init__(self, fname, x_train, y_train, corners=([10.0, 1500.0],[23.0, 6000.0]), verbose=1):
        self.verbose=verbose
        self.fname=fname
        if not os.path.exists(self.fname):
            os.makedirs(self.fname)
        self.x_train=x_train
        self.y_train=y_train
        self.corners=corners
        self.dists = ['Uniform(10., 23.)','Normal(4035., 400.)']
        # self.curv_abs=np.array([20000.])
    def buildK(self):
        if self.verbose>=1:
            print('\nConstructing Kriging surrogate model...')
        self.k_predictor = SurrogateModel('kriging', self.corners, global_optimizer=False)
        self.k_predictor.fit(self.x_train, self.y_train)
    def predictK(self,x_test):
        y_pred_krig, _ = self.k_predictor(x_test)
        print("y_pred_krig",y_pred_krig)

        # UQ
        if self.verbose>=1:
            print('\nDoing UQ...')
        k_uq = UQ(self.k_predictor, dists=self.dists, nsample=1000, plabels=['Ks', 'Q'], xlabel='s(km)', flabel='H(Ks,Q)', fname=self.fname+'/uqK')
        k_sobol = k_uq.sobol()
        if self.verbose>=1:
            print('Sobol indices: '+str(k_sobol))
        k_uq.error_propagation()

        # Visualization
        if self.verbose>=1:
            print('\nDoing some visusualizations...')

        # Response surface
        if self.verbose>=1:
            print('-> Response surface')
        response_surface(bounds=self.corners,
                         fun=lambda x: self.k_predictor(x)[0], flabel='H(Ks,Q)', plabels=['Ks', 'Q'],
                         feat_order=[1, 2], ticks_nbr=5, range_cbar=[-7.193, -0.159],
                         fname=self.fname+'/resp_surface_krig')


list_ks = [10,17,17,23,23,17,20,21,22,20,10,19,19,13,15,15,22,11,10,20,19,13,15]
list_q0 = [1500,1500,2000,2000,2350,2550,5000,4500,3700,4800,2300,4730,4730,2500, 3750,1500,3900,3300,5000,2500,3500,4700,2000]
list_q1 = [0,0,0,0,0,800,900,700,750,800,0,1000,800,20, 890,0,950,800,1000,30,850,750,0]
list_h = [9.51,8.00,8.65,7.82,8.28,9.93,10.97,10.62,10.11,10.87,10.24,10.99,10.93,9.85,10.96,8.37,10.35,11.20,11.99,8.79,10.37,11.44, 9.01]

x_train,y_train=parser(list_ks,list_q0,list_q1,list_h)

x_test=[[12.,2000.]]

S=Substitut('test',x_train,y_train)
S.buildK()
S.predictK(x_test)


## PC - LS
# degree=10
# init_size=x_train.shape[0]
# pc_predictor = batman.surrogate.SurrogateModel('LS', corners, n_samples=init_size, strategy='LS', degree=degree)
# pc_predictor.fit(x_train, y_train)
# y_pred_pc, _ = pc_predictor(x_test)
# print("y_pred_pc",y_pred_pc)
