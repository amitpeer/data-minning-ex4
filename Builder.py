import pandas as pd
import re


class Builder:
    def __init__(self):
        print("Builder ctr")
        self.attributes = {}

    def build(self, path, bin):
        self.readStructure(path + "\\Structure.txt")

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







        print("Builder.readStructure")
        with open(path, 'r') as structure:
            for line in structure:
                lineSplitBySpaces = line.split()
                self.attributes[lineSplitBySpaces[1]] = lineSplitBySpaces[2]
