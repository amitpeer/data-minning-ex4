import pandas as pd
import re
class Builder:

    def __init__(self):
        self.attributes = {}

        print("Builder ctr")



    def readStructure(self, path):
        file = open(path, 'r')




    def proccessData(self,path,bin):
        data = pd.read_csv(path);
        for att in self.attributes :
            if(self.attributes[att] == "NUMERIC") :
                #firs fill miss data with avarage value (use fillna and mean)
                data[att] = data.groupby("class").transform(lambda x: x.fillna(x.mean()))
                #now Discretization
                labels = range(bin+1)
                colBin = pd.cut(att, bins=bin, labels=labels, include_lowest=True)



             if(att == "class") :
                #we are in categorical attribute
                a=1
            else :
                a=1






