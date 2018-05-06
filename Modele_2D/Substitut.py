import os
import numpy as np
from sklearn.metrics import (r2_score, mean_squared_error)
import matplotlib.pyplot as plt
import batman
import openturns as ot
# from batman.functions.analytical import Channel_Flow
from batman.space import (Space, dists_to_ot)
from batman.uq import UQ
from batman.visualization import Kiviat3D, HdrBoxplot, response_surface, Tree
from batman.surrogate import SurrogateModel
from batman.surrogate import PC

ot.Log.Show(ot.Log.ERROR)

def reader(fileName, choice):
    list_ks=[]
    list_q=[]
    list_h=[]
    with open(fileName) as f:
        lines=f.readlines()
        for line in lines:
            tab=line.split(' ')
            if len(tab)==5:
                list_ks.append(tab[0].replace('\n',''))
                list_q.append(tab[1].replace('\n',''))
                list_h.append(tab[2+choice].replace('\n',''))
        return list_ks, list_q, list_h

def parser1(list_ks,list_q0,list_q1,list_h):
    x_train=[]
    y_train=[]
    for (ks,q0,q1,h) in zip(list_ks,list_q0,list_q1,list_h):
        x_train.append([float(ks),float(q0+q1)])
        y_train.append([float(h)])
    x_train=np.array(x_train)
    y_train=np.array(y_train)
    return x_train,y_train

def parser2(list_ks,list_q,list_h):
    x_train=[]
    y_train=[]
    for (ks,q,h) in zip(list_ks,list_q,list_h):
        x_train.append([float(ks),float(q)])
        y_train.append([float(h)])
    x_train=np.array(x_train)
    y_train=np.array(y_train)
    return x_train,y_train

class Substitut:
    def __init__(self, fname, x_train, y_train, corners=([10.0, 1500.0],[23.0, 6000.0]), verbose=1, dists=[ot.Uniform(17., 45.), ot.Normal(5750., 2075.)], dists_UQ=['Uniform(17., 45.)','Normal(5750., 2075.)']):
        self.verbose=verbose
        self.fname=fname
        if not os.path.exists(self.fname):
            os.makedirs(self.fname)
        self.x_train=x_train
        self.y_train=y_train
        self.corners=corners
        # self.dists = ['Uniform(10., 23.)','Normal(3750., 400.)']
        # self.dists = 
        self.dists = dists
        self.dists_UQ = dists_UQ
        # self.curv_abs=np.array([20000.])
    def buildK(self):
        if self.verbose >= 1:
            print('\nConstructing Kriging surrogate model...')
        self.k_predictor = SurrogateModel('kriging', self.corners, max_points_nb=1000, plabels=['Ks', 'Q'], global_optimizer=False)
        self.k_predictor.fit(self.x_train, self.y_train)
    def buildPC(self, degree):
        if self.verbose >= 1:
            print('\nConstructing Polynomial Chaos (PC) surrogate model...')
        init_size=self.x_train.shape[0]
        # P= int(np.sqrt(init_size)-1)
        P=degree
        print("P="+str(P))
        # self.pc_predictor = SurrogateModel('pc', self.corners, max_points_nb=1000, plabels=['Ks', 'Q'], sample=init_size, strategy='LS', degree=P, distributions=self.dists)
        self.pc_predictor = SurrogateModel('pc', self.corners, max_points_nb=1000, plabels=['Ks', 'Q'], sample=init_size, strategy='LS', degree=P, distributions=self.dists)
        self.pc_predictor.fit(self.x_train, self.y_train)
    def predictK(self,x_test):
        y_pred_krig, _ = self.k_predictor(x_test)
        return y_pred_krig
    def predictPC(self,x_test):
        y_pred_pc, _ = self.pc_predictor(x_test)
        return y_pred_pc
    def analysisK(self):
        # UQ
        if self.verbose >= 1:
            print('\nDoing UQ...')
        k_uq = UQ(self.k_predictor, dists=self.dists_UQ, nsample=1000*0+10000, plabels=['Ks', 'Q'], xlabel='s(km)', flabel='H(Ks,Q)', fname=self.fname+'/uqK')
        k_sobol = k_uq.sobol()
        # second, first, total
        if self.verbose >= 1:
            print('Sobol indices: '+str(k_sobol))
        k_uq.error_propagation()

        # Visualization
        if self.verbose >= 1:
            print('\nDoing some visusualizations...')

        # Response surface
        if self.verbose >= 1:
            print('-> Response surface')
        """response_surface(bounds=self.corners,
                         fun=lambda x: self.k_predictor(x)[0], flabel='H(Ks,Q)', plabels=['Ks', 'Q'],
                         feat_order=[1, 2], ticks_nbr=5, range_cbar=[-7.193, -0.159],
                         fname=self.fname+'/resp_surface_krig')"""
        response_surface(bounds=self.corners,
                         fun=lambda x: self.k_predictor(x)[0], flabel='H(Ks,Q)', plabels=['Ks', 'Q'],
                         feat_order=[1, 2], ticks_nbr=5, doe=self.x_train,
                         fname=self.fname+'/resp_surface_krig')
    def analysisPC(self):
        # UQ
        if self.verbose >= 1:
            print('\nDoing UQ...')
        pc_uq = UQ(self.pc_predictor, dists=self.dists_UQ, nsample=1000*0+10000, plabels=['Ks', 'Q'], xlabel='s(km)', flabel='H(Ks,Q)', fname=self.fname+'/uqPC')
        pc_sobol = pc_uq.sobol()
        # second, first, total
        if self.verbose >= 1:
            print('Sobol indices: '+str(pc_sobol))
        pc_uq.error_propagation()

        # Visualization
        if self.verbose >= 1:
            print('\nDoing some visusualizations...')

        # Response surface
        if self.verbose >= 1:
            print('-> Response surface')
        """response_surface(bounds=self.corners,
                         fun=lambda x: self.k_predictor(x)[0], flabel='H(Ks,Q)', plabels=['Ks', 'Q'],
                         feat_order=[1, 2], ticks_nbr=5, range_cbar=[-7.193, -0.159],
                         fname=self.fname+'/resp_surface_krig')"""
        response_surface(bounds=self.corners,
                         fun=lambda x: self.pc_predictor(x)[0], flabel='H(Ks,Q)', plabels=['Ks', 'Q'],
                         feat_order=[1, 2], ticks_nbr=5, doe=self.x_train,
                         fname=self.fname+'/resp_surface_pc')


"""def estimateLOOError(list_ks, list_q, list_h, list_h_pred, verbose=0):
    list_err=[]
    err=0.
    for i,(ks,q,h) in enumerate(zip(list_ks,list_q,list_h)):
        list_ks_tmp=list_ks[:]
        list_q_tmp=list_q[:]
        list_h_tmp=list_h[:]
        ks=float(list_ks_tmp.pop(i))
        q=float(list_q_tmp.pop(i))
        h=float(list_h_tmp.pop(i))
        x_train,y_train=parser2(list_ks_tmp,list_q_tmp,list_h_tmp)
        x_test=[[ks,q]]

        if verbose:
            print("y_pred="+str(list_h_pred[i])+"\t h="+str(h)+"\t err(%)="+str((list_h_pred[i]-h)/h))
        err+=(list_h_pred[i]-h)**2.
        list_err.append((list_h_pred[i]-h)/h)
    err/=len(list_h)
    if verbose:
        print("err="+str(err))
    return err, list_err"""