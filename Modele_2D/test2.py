from Substitut import *


list_ks=[]
list_q=[]
list_h=[]

choice=0

with open('data2.txt') as f:
    lines=f.readlines()
    for line in lines:
        tab=line.split(' ')
        # print(tab)
        if len(tab)==5:
            list_ks.append(tab[0].replace('\n',''))
            list_q.append(tab[1].replace('\n',''))
            list_h.append(tab[2+choice].replace('\n',''))
print("Ks : "+str(min(list_ks))+" \t "+str(max(list_ks)))
print("Q : "+str(min(list_q))+" \t "+str(max(list_q)))

# print(list_ks)
# print(list_q)
# print(list_h)

# x_train,y_train=parser2(list_ks,list_q,list_h)

# print(x_train)
# print(y_train)

# x_test=[[12.,2000.]]
# x_test=[[27.492280248943413,6991.18916274119]]

# S=Substitut('test',x_train,y_train)
# S.buildK()
# y_pred_krig=S.predictK(x_test)


corners=([15.,1500.],[50.,10000.])

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

    S=Substitut('test',x_train,y_train,corners=corners,verbose=0)
    S.buildK()
    y_pred_krig=S.predictK(x_test)[0,0]
    print("y_pred_krig="+str(y_pred_krig)+"\t h="+str(h)+"\t err(%)="+str((y_pred_krig-h)/h))
    err+=(y_pred_krig-h)**2.
    """if i==5:
        break"""
err/=len(list_h)
print("err="+str(err))

x_train,y_train=parser2(list_ks,list_q,list_h)
x_test=[[12.,2000.]]
S=Substitut('test',x_train,y_train,corners=corners)
S.buildK()
y_pred_krig=S.predictK(x_test)[0,0]
print("y_pred_krig="+str(y_pred_krig))
S.analysisK()



## PC - LS
# degree=10
# init_size=x_train.shape[0]
# pc_predictor = batman.surrogate.SurrogateModel('LS', corners, n_samples=init_size, strategy='LS', degree=degree)
# pc_predictor.fit(x_train, y_train)
# y_pred_pc, _ = pc_predictor(x_test)
# print("y_pred_pc",y_pred_pc)
