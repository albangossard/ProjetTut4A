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
        with open(path+'output/snapshots/'+str(i)+'/sample-data.json') as jsonData:
            data=json.load(jsonData)
            self.__X=data['X']
        self.__structIn={"space":{"sampling":{"init_size","method","distributions"}},
                    "pod":{"dim_max","tolerance"},
                    "surrogate":{"predictions","method","strategy"}
                }
        with open(path+'settings.json') as jsonData:
            data=json.load(jsonData)
            self.__paramIn={}
            for block in self.__structIn:
                self.__paramIn[block]={}
                if isinstance(self.__structIn[block], dict):
                    for subblock in self.__structIn[block]:
                        self.__paramIn[block][subblock]={}
                        for e in self.__structIn[block][subblock]:
                            self.__paramIn[block][subblock][e]=data[block][subblock][e]
                else:
                    for e in self.__structIn[block]:
                        self.__paramIn[block][e]=data[block][e]
    def getSpacePts(self):
        return self.__X
    def getDataOut(self,id=None):
        if id==None:
            return self.__x1,self.__x2,self.__F
        else:
            return self.__x1[id],self.__x2[id],self.__F[id]
    def getParamIn(self,param,block,subblock=None):
        if subblock==None:
            return self.__paramIn[block][param]
        else:
            return self.__paramIn[block][subblock][param]
    def getParamInText(self):
        listTxt=[]
        for block in self.__structIn:
            txt=""
            if isinstance(self.__structIn[block], dict):
                for subblock in self.__structIn[block]:
                    for e in self.__structIn[block][subblock]:
                        txt+=e+"="+str(self.__paramIn[block][subblock][e])+"   "
            else:
                for e in self.__structIn[block]:
                    txt+=e+"="+str(self.__paramIn[block][e])+"   "
            listTxt.append(txt)
        return listTxt
