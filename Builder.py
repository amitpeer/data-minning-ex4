import pandas as pd

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
        self.trainingSet = self.proccessData(self.path + "/train.csv", True)

    def isBinValid(self):
        return self.trainingSet

    def readTestSet(self):
        print("readTestSet")
        self.testSet = self.proccessData(self.path + "/test.csv", False)

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

    def isValidBin(self,myData) :
        minBin = 1
        distanceValue = 1
        for att in self.attributes :
            if self.attributes[att] == "NUMERIC":
                distanceValue = myData[att].max() - myData[att].min()
                if distanceValue>minBin :
                    minBin=distanceValue
        return distanceValue > self.bins

    # fill missing values + discrimination
    def proccessData(self, path, isTrainSet):
        print("proccessData")
        data = pd.read_csv(path)

        for att in data:
            if (self.attributes[att] == "NUMERIC"):

                #check Bins on trainning set
                if self.bins > data[att].max() - data[att].min() and isTrainSet:
                    return None

                # fill miss data with avarage value (use fillna and mean)
                data[att] = data.groupby("class").transform(lambda x: x.fillna(x.mean()))[att]

                # Discretization
                data[att] = pd.cut(data[att], bins=self.bins, labels=False)

            elif (att != "class"):
                # categorical issue
                fillEmptyWith = None
                if len(data[att].mode()) == 0:
                    # Case there is equal number of different values
                    fillEmptyWith = self.attributes[att][0]
                else :
                    fillEmptyWith = data[att].mode()[0]
                data[att].fillna(fillEmptyWith, inplace=True)

        return data
