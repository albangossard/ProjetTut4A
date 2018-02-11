from batmanIO import *

simul=batmanIO('')
simul.read()
print(simul.getParamIn("distributions","space","sampling")[0])
print(simul.getParamIn("predictions","surrogate"))
print(simul.getSpacePts())
x1,x2,F=simul.getDataOut()
print(x1)
print(x2)
print(F)