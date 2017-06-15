import pandas as pd


class Classifier:
    def __init__(self, builder):
        print("Classifier ctr")
        self.builder = builder
        self.trainingSet = builder.trainingSet
        self.testSet = builder.testSet
        self.attributes = builder.attributes
        self.m = 2
        self.numberOfDifferentClassses = None

    def calssify(self):
        print("classify")
        self.numberOfDifferentClassses = self.trainingSet.groupby("class")['class'].agg('count')
        self.numberOfRows = len(self.trainingSet["class"])
        allProbsArray = []
        for rowNumber in range(len(self.testSet["class"])):

            # calulate probability for each attribute
            for att in self.testSet:
                if (att != 'class'):
                    value = self.testSet[att][rowNumber]
                    propsArray = self.mEstimate(att, value)
                    allProbsArray.insert(len(allProbsArray), propsArray)

            # multiplie same class and find final probability
            sameClassProbs = []
            for val in range(len(allProbsArray[0])):
                multiplieProp = 1.0
                for probsArr in allProbsArray:
                    multiplieProp *= probsArr[val]
                sameClassProbs.insert(len(sameClassProbs),
                                      self.numberOfDifferentClassses[val] / self.numberOfRows *
                                      multiplieProp)

            # find max
            maxValueIndex = sameClassProbs.index(max(sameClassProbs))
            classification = self.attributes['class'][maxValueIndex]
            with open(self.builder.path + "\\output.txt", 'a') as output:
                output.write(str(rowNumber) + " " + classification + "\n")

        print("Finished classifying all rows")

    def mEstimate(self, att, value):
        print("mEstimate")
