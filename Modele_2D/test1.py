from Substitut import *


list_ks = [10,17,17,23,23,17,20,21,22,20,10,19,19,13,15,15,22,11,10,20,19,13,15]
list_q0 = [1500,1500,2000,2000,2350,2550,5000,4500,3700,4800,2300,4730,4730,2500, 3750,1500,3900,3300,5000,2500,3500,4700,2000]
list_q1 = [0,0,0,0,0,800,900,700,750,800,0,1000,800,20, 890,0,950,800,1000,30,850,750,0]
list_h = [9.51,8.00,8.65,7.82,8.28,9.93,10.97,10.62,10.11,10.87,10.24,10.99,10.93,9.85,10.96,8.37,10.35,11.20,11.99,8.79,10.37,11.44, 9.01]

x_train,y_train=parser1(list_ks,list_q0,list_q1,list_h)

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
