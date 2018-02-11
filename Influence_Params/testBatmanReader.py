from batmanReader import *

pred=batmanReader('')
print(pred.getParamIn("distributions","space","sampling")[0])
print(pred.getParamIn("predictions","surrogate"))
print(pred.getSpacePts())
x1,x2,F=pred.getDataOut()
print(x1)
print(x2)
print(F)