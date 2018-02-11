import json, os
import numpy as np

class batmanReader:
    def __init__(self,path):
        dirs = [f for f in os.listdir(path+'output/predictions') if not os.path.isfile(f)]
        nbDir=len(dirs)
        self.__F=[]
        self.__x1=[]
        self.__x2=[]
        for i in range(nbDir):
            with open(path+'output/predictions/Newsnap'+str(i)+'/sample-data.json') as jsonData:
                data=json.load(jsonData)
                self.__F.append(data['F'])
            with open(path+'output/predictions/Newsnap'+str(i)+'/sample-space.json') as jsonData:
                data=json.load(jsonData)
                self.__x1.append(data['x1'][0])
                self.__x2.append(data['x2'][0])
        structIn={"space":{"sampling":{"init_size","method","distributions"}},
                    "pod":{"dim_max","tolerance"},
                    "surrogate":{"predictions","method","strategy"}
                }
        with open(path+'settings.json') as jsonData:
            data=json.load(jsonData)
            self.__paramIn={}
            for block in structIn:
                self.__paramIn[block]={}
                if type(structIn[block])=='dict':
                    for subblock in structIn[block]:
                        self.__paramIn[block][subblock]={}
                        for e in structIn[block][subblock]:
                            self.__paramIn[block][subblock][e]=data[block][subblock][e]
                else:
                    for e in structIn[block]:
                        self.__paramIn[block][e]=data[block][e]
    def getData(self,id=None):
        if id==None:
            return self.__x1,self.__x2,self.__F
        else:
            return self.__x1[id],self.__x2[id],self.__F[id]
    def getParamIn(self,param,block,subblock=None):
        if subblock==None:
            return self.__paramIn[block][param]
        else:
            return self.__paramIn[block][subblock][param]

pred=predictionsReader('')
print(pred.getParamIn("distributions","space","sampling")[0])
print(pred.getParamIn("predictions","surrogate"))
x1,x2,F=pred.getData()
print(x1)
print(x2)
print(F)