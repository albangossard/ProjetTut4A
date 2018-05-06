import os
import sys
import openturns as ot
import numpy as np
from batman.visualization import response_surface
from batman.surrogate import SurrogateModel

ot.Log.Show(ot.Log.ERROR)

options = [sys.argv[i+1] for i in range(len(sys.argv)-1)]


def build_training_set(ks_values, q_values, h_values):
    """Build the training input set and the training output set for the Garonne
    case test where the inputs are the friction coefficient Ks and the upstream
    discharge Q and where the output is the waterlevel h at a given location.

    :param list(float) ks_values: N values of Ks.
    :param list(float) q_values: N values of Q.
    :param list(float) h_values: N values of h.
    :return  hydraulic_state: dictionnary containing
        curvilinear abscissa, water level and flowrate
    :return list(list(float)) x_train: N values of [Ks, Q]
            list(list(float)) y_train: N values of [h]
    """
    x_train = []
    y_train = []
    if type(q_values[0]) is list:
        q0_values = q_values[0]
        q1_values = q_values[1]
        for (ks, q0, q1, h) in zip(ks_values, q0_values, q1_values, h_values):
            x_train.append([float(ks), float(q0+q1)])
            y_train.append([float(h)])
    else:
        for (ks, q, h) in zip(ks_values, q_values, h_values):
            x_train.append([float(ks), float(q)])
            y_train.append([float(h)])
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    return x_train, y_train


class UQStudy:
    def __init__(self, fname, x_train, y_train,
                 corners=([17.0, 1600.0], [45.0, 9900.0]), verbose=1):
        self.verbose = verbose
        self.fname = fname
        if not os.path.exists(self.fname):
            os.makedirs(self.fname)
        self.x_train = x_train
        self.y_train = y_train
        self.corners = corners
        #self.dists = ['Uniform(17., 45.)', 'Normal(5750., 410.)']
        self.dists = [ot.Uniform(17., 45.), ot.Normal(5750., 410.)]

    def buildK(self):
        if self.verbose >= 1:
            print('\nConstructing Kriging surrogate model...')
        self.k_predictor = SurrogateModel('kriging', self.corners,
                                          max_points_nb=1000,
                                          plabels=['Ks', 'Q'],
                                          global_optimizer=False)
        self.k_predictor.fit(self.x_train, self.y_train)

    def buildPC(self):
        if self.verbose >= 1:
            print('\nConstructing Polynomial Chaos (PC) surrogate model...')
        init_size = self.x_train.shape[0]
        P = int(np.sqrt(init_size)-1)
        self.pc_predictor = SurrogateModel('pc', self.corners,
                                           max_points_nb=1000,
                                           plabels=['Ks', 'Q'],
                                           sample=init_size, strategy='LS',
                                           degree=P, distributions=self.dists)
        self.pc_predictor.fit(self.x_train, self.y_train)

    def predictK(self, x_test):
        y_pred_krig, _ = self.k_predictor(x_test)
        return y_pred_krig

    def predictPC(self, x_test):
        y_pred_pc, _ = self.pc_predictor(x_test)
        return y_pred_pc

    def responseSurfaceK(self):
        response_surface(bounds=self.corners,
                         fun=lambda x: self.k_predictor(x)[0],
                         flabel='H(Ks, Q)',
                         plabels=['Ks', 'Q'],
                         feat_order=[1, 2],
                         ticks_nbr=5,
                         doe=self.x_train,
                         fname=self.fname+'/resp_surface_krig')
        
    def responseSurfacePC(self):
        response_surface(bounds=self.corners,
                         fun=lambda x: self.pc_predictor(x)[0],
                         flabel='H(Ks, Q)',
                         plabels=['Ks', 'Q'],
                         feat_order=[1, 2],
                         ticks_nbr=5,
                         doe=self.x_train,
                         fname=self.fname+'/resp_surface_pc')

    def analysisK(self):
        # UQ
        """if self.verbose>=1:
            print('\nDoing UQ...')
        k_uq = UQ(self.k_predictor, dists=self.dists, nsample=1000,
        plabels=['Ks', 'Q'], xlabel='s(km)', flabel='H(Ks,Q)',
        fname=self.fname+'/uqK')
        k_sobol = k_uq.sobol()"""
        # second, first, total
        """if self.verbose>=1:
            print('Sobol indices: '+str(k_sobol))
        k_uq.error_propagation()"""

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
                         fun=lambda x: self.k_predictor(x)[0],
                         flabel='H(Ks,Q)',
                         plabels=['Ks', 'Q'],
                         feat_order=[1, 2],
                         ticks_nbr=5,
                         doe=self.x_train,
                         fname=self.fname+'/resp_surface_krig')

if __name__ == "__main__":

    ks_values = []
    q_values = []
    h_values = []

    # There are three  spatial points of interest indexed (output_index in
    # {1,2,3}) where we want to study the water level.
    output_index = 0

    with open('data2.txt') as f:
        lines = f.readlines()
        for line in lines:
            tab = line.split(' ')
            if len(tab) == 5:
                ks_values.append(tab[0].replace('\n', ''))
                q_values.append(tab[1].replace('\n', ''))
                h_values.append(tab[2+output_index].replace('\n', ''))

    print("min(Ks) = {} - max(Ks) = {}".format(min(ks_values), max(ks_values)))
    print("min(Q) = {} - max(Q) = {}".format(min(q_values), max(q_values)))

    Ks_corners = [15., 1500.]
    Q_corners = [45., 10000.]
    corners = (Ks_corners, Q_corners)

    # Build the input and output learning sets.
    x_train, y_train = build_training_set(ks_values, q_values, h_values)

    if 'k' in options:
        # Run the UQ study using a model "Kriging".
        # -- Initialize input and output learning sets and corners.
        study_from_K = UQStudy('test', x_train, y_train, corners)
        # -- Build the model "Kriging".
        study_from_K.buildK()
        # --- Build the response surface
        study_from_K.responseSurfaceK()

    if 'pc' in options:
        # Run the UQ study using a model "Polynomial Chaos Expansion".
        # -- Initialize input and output learning sets and corners.
        study_from_PC = UQStudy('test', x_train, y_train, corners)
        # -- Build the surrogate model "Polynomial Chaos Expansion".
        study_from_PC.buildPC()
        # --- Build the response surface
        study_from_PC.responseSurfacePC()
