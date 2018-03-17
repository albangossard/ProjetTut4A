"""Showcase API."""
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


def fl(x,f):
    """Omit boundary condition."""
    return f(x)[:, :-1]


class Analyse:
    def __init__(self, fname, corners=([15.0, 2500.0],[60.0, 6000.0]), init_size=25, verbose=1):
        self.fname=fname
        self.verbose=verbose
        if not os.path.exists(self.fname):
            os.makedirs(self.fname)
        # Test function
        self.f = Channel_Flow(dx=8000., length=40000.)  # Change dx to increase discretization
        self.curv_abs = self.f.x[:-1]  # Omit boundary condition
        # Parameter space
        if self.verbose>=1:
            print('Constructing parameter space and the training data...')
        self.corners = corners  # ([min(X1), min(X2)], [max(X1), max(X2)])
        self.init_size = init_size  # training sample size
        # indim = len(corners[0])  # inputs dim
        plabels = ['Ks', 'Q']
        self.space = Space(self.corners, self.init_size, plabels=plabels)
        # Build the learning sample
        self.x_train = np.array(self.space.sampling(self.init_size, 'halton'))
        self.y_train = fl(self.x_train,self.f)
        if self.verbose>=1:
            print(repr(self.space))
        self.space.write(self.fname+'/space-values.dat')
    def test(self, test_size=1000, dists=['Uniform(15., 60.)','Normal(4035., 400.)']):
        # Build the test sample
        if self.verbose>=1:
            print('Constructing testing data...')
        self.test_size = test_size  # test size
        self.dists = dists
        self.dists_ot = dists_to_ot(self.dists)
        self.x_test = ot.LHSExperiment(ot.ComposedDistribution(self.dists_ot), self.test_size, True, True).generate()
        self.x_test = np.array(self.x_test)
        self.y_test = fl(self.x_test,self.f)
    def surrogateKriging(self):
        # Kriging
        # Surrogate
        if self.verbose>=1:
            print('\nConstructing Kriging surrogate model...')
        #k_predictor = SurrogateModel('kriging', corners, init_size, global_optimizer=False)
        k_predictor = SurrogateModel('kriging', self.corners, global_optimizer=False)
        k_predictor.fit(self.x_train, self.y_train)
        y_pred_krig, _ = k_predictor(self.x_test)

        # Error
        if self.verbose>=1:
            print('Getting metrics:')
        self.mseKriging = mean_squared_error(self.y_test, y_pred_krig)
        self.q2Kriging = r2_score(self.y_test, y_pred_krig)
        if self.verbose>=1:
            print('-> MSE: '+str(self.mseKriging)+'\n-> Q2: '+str(self.q2Kriging))

        # UQ
        if self.verbose>=1:
            print('\nDoing UQ...')
        k_uq = UQ(k_predictor, dists=self.dists, nsample=1000, plabels=['Ks', 'Q'], xlabel='s(km)', flabel='H(Ks,Q)', xdata=self.curv_abs, fname=self.fname+'/uqK')
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
        response_surface(bounds=([30.0, 3000.0], [55.0, 5500.0]),
                         fun=lambda x: k_predictor(x)[0], flabel='H(Ks,Q)', plabels=['Ks', 'Q'],
                         feat_order=[1, 2], ticks_nbr=5, range_cbar=[-7.193, -0.159],
                         fname=self.fname+'/resp_surface_krig', xdata=self.curv_abs)
    def surrogatePC(self, strg='Quad', degree=5):
        # Polynomial Chaos
        # Surrogate
        self.strg = strg
        self.degree=degree
        if self.verbose>=1:
            print('\nConstructing Polynomial Chaos ('+str(self.strg)+') surrogate model...')
        if (self.strg == 'Quad'):
            pc_predictor = PC(strategy='Quad', degree=self.degree, distributions=self.dists_ot)
            self.x_train = pc_predictor.sample
            self.y_train = fl(self.x_train,self.f)
            pc_predictor.fit(self.x_train, self.y_train)
            y_pred_pc = pc_predictor.evaluate(self.x_test)
        else:
            pc_predictor = batman.surrogate.SurrogateModel('LS', self.corners, self.init_size, strategy='LS', degree=self.degree, distributions=self.dists_ot)
            pc_predictor.fit(self.x_train, self.y_train)
            y_pred_pc, _ = pc_predictor(self.x_test)

        # Error
        if self.verbose>=1:
            print('Getting metrics:')
        self.msePC = mean_squared_error(self.y_test, y_pred_pc)
        self.q2PC = r2_score(self.y_test, y_pred_pc)
        if self.verbose>=1:
            print('-> MSE: '+str(self.msePC)+'\n-> Q2: '+str(self.q2PC))

        """# UQ
        if self.verbose>=1:
            print('\nDoing UQ...')
        pc_uq = UQ(pc_predictor, dists=self.dists, nsample=1000, plabels=['Ks', 'Q'], xlabel='s(km)', flabel='H(Ks,Q)', xdata=self.curv_abs, fname=self.fname+'/uqPC')
        pc_sobol = pc_uq.sobol()
        if self.verbose>=1:
            print('Sobol indices: '+str(pc_sobol))
        pc_uq.error_propagation()

        # Visualization
        if self.verbose>=1:
            print('\nDoing some visusualizations...')

        # Response surface
        if self.verbose>=1:
            print('-> Response surface')
        response_surface(bounds=([30.0, 3000.0], [55.0, 5500.0]),
                         fun=lambda x: pc_predictor(x)[0], flabel='H(Ks,Q)', plabels=['Ks', 'Q'],
                         feat_order=[1, 2], ticks_nbr=5, range_cbar=[-7.193, -0.159],
                         fname=self.fname+'/resp_surface_pc', xdata=self.curv_abs)"""
    def getSensibilityPC(self):
        return self.msePC,self.q2PC
    def getSensibilityKriging(self):
        return self.mseKriging,self.q2Kriging




# HDR
"""print('-> HDR')
hdr = HdrBoxplot(y_train, variance=0.9, optimize=True)
hdr.plot(x_common=curv_abs, xlabel='Curvilinear abscissa (km)',
         flabel='Water level (m)', fname='hdr.pdf')
hdr.f_hops()
hdr.sound()"""

# Kiviat
"""print('-> Kiviat')
kiviat = Kiviat3D(space, y_train, bounds=corners, plabels=['Ks', 'Q', '-'])
kiviat.plot(flabel='Water level (m)', fname='kiviat.pdf')"""

# Tree
"""print('-> Tree')
tree = Tree(space, y_train, bounds=corners, plabels=['Ks', 'Q'])
tree.plot(flabel='Water level (m)', fname='tree.pdf')"""

