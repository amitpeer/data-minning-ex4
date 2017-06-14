import pandas as pd
import scipy.stats as stats
import re


class Builder:
    def __init__(self, path, bins):
        print("Builder ctr")
        self.attributes = {}
        self.path = path
        self.bins = bins
        self.trainingSet = None
        self.testSet = None

    def build(self):
        self.readStructure()
        self.arrangeAttributes()
        self.trainingSet = self.proccessData(self.path + "/train.csv")

    def readTestSet(self):
        print("readTestSet")
        self.testSet = self.proccessData(self.path + "/test.csv")

    def readStructure(self):
        print("Builder.readStructure")
        path = self.path + "/Structure.txt"
        with open(path, 'r') as structure:
            for line in structure:
                lineSplitBySpaces = line.split()
                self.attributes[lineSplitBySpaces[1]] = lineSplitBySpaces[2]

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
    def proccessData(self, path):
        print("proccessData")
        data = pd.read_csv(path)
        for att in data:
            if (self.attributes[att] == "NUMERIC"):

                # fill miss data with avarage value (use fillna and mean)
                data[att] = data.groupby("class").transform(lambda x: x.fillna(x.mean()))[att]

                # Discretization
                data[att] = self.discretization(data[att])
                # data[att] = pd.cut(data[att], bins=self.bins, labels=False)

                # change "numeric" to the values after discrimination
                self.attributes[att] = range(0, self.bins)

            elif (att != "class"):
                # categorical issue
                data[att].fillna(data[att].mode()[0], inplace=True)

        for var in data:
            print(data[var])
        return data

    def discretization(self, col):
        minval = col.min()
        maxval = col.max()
        weight = (maxval - minval) / self.bins
        break_points = [minval]  # initialize  list
        for i in range(0, self.bins):
            # insert interval to list
            break_points.insert(len(break_points), minval + (i+1) * weight + 1)
            # minval = minval + interval

        # break_points.insert(len(break_points), maxval)
        labels = range(len(break_points) - 1)  # the labels of the bins
        colbins = pd.cut(col, bins=break_points, labels=labels, include_lowest=True)

        return colbins
