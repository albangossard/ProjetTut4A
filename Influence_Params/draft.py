class snapshotsReader:
    def __init__(self,path):
        dirs = [f for f in os.listdir(path) if not os.path.isfile(f)]
        dirs=list(map(int, dirs))
        nbDir=np.array(dirs).max()+1
        print(nbDir)
        self.__data=[]
        self.__X=[]
        self.__F=[]
        self.__x1=[]
        self.__x2=[]
        for i in range(nbDir):
            with open(path+'/'+str(i)+'/sample-data.json') as jsonData:
                data=json.load(jsonData)
                self.__X.append(data['X'])
                self.__F.append(data['F'])
            with open(path+'/'+str(i)+'/sample-space.json') as jsonData:
                data=json.load(jsonData)
                self.__x1.append(data['x1'][0])
                self.__x2.append(data['x2'][0])
            # self.__data__.append(np.array([x1,x2,np.array(X),np.array(F)]))
        # self.__data__=np.array(self.__data__)
        # for line in self.__data__:
        #     print(line)
    def getParamRange(self,param=0):
        if param==0:
            return (sorted(set(self.__x1)),sorted(set(self.__x2)))
        elif param==1:
            return sorted(set(self.__x1))
        else:
            return sorted(set(self.__x2))

# snap=snapshotsReader('Tests/Channel_Flow/output/snapshots')
# x1Range,x2Range=snap.getParamRange()
# print(x1Range)
# print(x2Range)