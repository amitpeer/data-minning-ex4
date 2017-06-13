import pandas as pd
import re


class Builder:
    def __init__(self):
        print("Builder ctr")
        self.attributes = {}

    def build(self, path, bin):
        self.readStructure(path + "\\Structure.txt")
        self.proccessData(path + "\\train.cvs",bin)



    def readStructure(self, path):
        file = open(path, 'r')

        print("Builder.readStructure")
        with open(path, 'r') as structure:
            for line in structure:
                lineSplitBySpaces = line.split()
                self.attributes[lineSplitBySpaces[1]] = lineSplitBySpaces[2]



    def proccessData(self,path,bin):
        data = pd.read_csv(path);
        for att in self.attributes :
            if(self.attributes[att] == "NUMERIC"):
                #firs fill miss data with avarage value (use fillna and mean)
                data[att] = data.groupby("class").transform(lambda x: x.fillna(x.mean()))
                #now Discretization
                labels = range(bin+1)
                data[att] = pd.cut(data[att], bins=bin, labels=labels, include_lowest=True)
            if(att == "class") :
                 #use array and not string
                clasiffication = self.attributes[att][1:-1]
                clasiffication = clasiffication.split(',')
                self.attributes[att] = clasiffication
            else :
                #categorical issue
                attribute = self.attributes[att][1:-1]
                attribute = attribute.split(',')
                self.attributes[att] = attribute
                data[att].fillna(data[att].mode[0], inplace=True)
        print(data)






