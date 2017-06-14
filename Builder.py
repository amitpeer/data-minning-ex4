import pandas as pd
import scipy.stats as stats
import re


class Builder:
    def __init__(self):
        print("Builder ctr")
        self.attributes = {}

    def build(self, path, bin):
        self.readStructure(path + "/Structure.txt")
        self.arrangeAttributes()
        self.traningSet = self.proccessData(path + "/train.csv", bin)

    def readStructure(self, path):
        print("Builder.readStructure")
        file = open(path, 'r')
        with open(path, 'r') as structure:
            for line in structure:
                lineSplitBySpaces = line.split()
                self.attributes[lineSplitBySpaces[1]] = lineSplitBySpaces[2]

    def discretization(self, col, bins):
        minval = col.min()
        maxval = col.max()
        interval = (maxval-minval)/bins
        break_points = [minval]
        for i in range(0,bins):
            break_points.insert(minval+interval)
            minval = minval+interval

        break_points.insert(maxval)
        labels = range(len(break_points)-1)
        colbins = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)
        return colbins

    # arrange attributes dictionary so all the attributes values would be in array
    def arrangeAttributes(self):
        print("arrangeAttributes")
        for att in self.attributes:
            if (self.attributes[att] != "NUMERIC"):
                attribute = self.attributes[att][1:-1]
                attribute = attribute.split(',')
                self.attributes[att] = attribute
        for key, value in self.attributes.items():
            print(key, value)

    # fill missing values + discrimination
    def proccessData(self, path, bin):
        print("proccessData")
        data = pd.read_csv(path)
        for att in data:
            if (self.attributes[att] == "NUMERIC"):
                # fill miss data with avarage value (use fillna and mean)
                data[att] = data.groupby("class").transform(lambda x: x.fillna(x.mean()))

                # Discretization
                #data[att] = discretization(data[att], bin)
                data[att] = pd.cut(data[att], bins=bin, labels=False)

                # change "numeric" to the values after Discertization
                self.attributes[att] = range(0, bin)

            elif (att != "class"):
                # categorical issue
                data[att].fillna(data[att].mode()[0], inplace=True)

        for var in data:
            print(data[var])
        return data



