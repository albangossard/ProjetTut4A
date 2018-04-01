from Analyse import *

A=Analyse('test',init_size=180*0+10)
A.test()
# A.surrogateKriging()
A.surrogatePC(degree=2)
A.surrogatePC(strg='LS',degree=2)