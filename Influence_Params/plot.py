from batmanReader import *
import matplotlib.pyplot as plt

def plotInfo(plt,listTxt):
    for i,txt in enumerate(listTxt):
        plt.figtext(0.0, 1.-0.05*i,txt, wrap=True,
                    horizontalalignment='left', fontsize=8)

pred=batmanReader('')
print(pred.getParamIn("distributions","space","sampling")[0])
print(pred.getParamIn("predictions","surrogate"))
X=pred.getSpacePts()
x1,x2,F=pred.getDataOut()
print(x1)
print(x2)
print(F)

for i in range(len(F)):
    plt.plot(X,F[i],label='x1='+str(x1[i])+' x2='+str(x2[i]))
plt.legend()
plotInfo(plt,pred.getParamInText())
plt.xlabel("X")
plt.ylabel("h")
plt.show()