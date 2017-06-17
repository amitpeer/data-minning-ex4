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
        self.numberOfRows = None
        self.allCalcs = {}

    def calculate(self):
        print("calculate")

        for att in self.attributes:
            if att != 'class':
                self.allCalcs[att] = {}
                differentValues = self.testSet.groupby(att)['class'].agg('count')
                allAttval = self.trainingSet.groupby([att])[att].agg('count')  # needed to calc p
                m = 2.0
                p = 1.0 / len(allAttval)

                for value in differentValues.keys():
                    self.allCalcs[att][value] = {}

                    for classValue in self.attributes['class']:
                        n = float(self.numberOfDifferentClassses[classValue])
                        nc = self.trainingSet[(self.trainingSet[att] == value)
                                              & (self.trainingSet['class'] == classValue)][att].count()
                        self.allCalcs[att][value][classValue] = (nc + m * p) / (n + m)

    def classify2(self):
        print("classify2")
        allProbsArray = []
        for rowNumber in range(len(self.testSet["class"])):
            print(rowNumber)
            for att in self.testSet:
                if att != 'class':
                    value = self.testSet[att][rowNumber]
                    propsArray = self.allCalcs[att][value]
                    allProbsArray.append(propsArray)

            sameClassProbs = []
            classValueIndex = 0
            for classValue in self.attributes['class']:
                multiplieProp = 1.0
                for probsArr in allProbsArray:
                    multiplieProp *= probsArr[self.attributes["class"][classValueIndex]]

                sameClassProbs.insert(len(sameClassProbs),
                                    float(self.numberOfDifferentClassses[classValue])
                                    / float(self.numberOfRows) *
                                    multiplieProp)

                classValueIndex = classValueIndex + 1

            # find max
            maxValueIndex = sameClassProbs.index(max(sameClassProbs))
            # classification = self.attributes['class'][maxValueIndex]
            classification = self.attributes['class'][maxValueIndex]
            with open(self.builder.path + "\\output.txt", 'a') as output:
                output.write(str(rowNumber) + " " + classification + "\n")
        print("Finished classifying all rows")
        self.accuracy()



    def calssify(self):
        print("classify")
        self.numberOfDifferentClassses = self.trainingSet.groupby("class")['class'].agg('count')
        self.numberOfRows = len(self.trainingSet["class"])
        self.calculate()
        self.classify2()
        # allProbsArray = []
        # for rowNumber in range(len(self.testSet["class"])):
        #     # for rowNumber in range(5):
        #     print(rowNumber)
        #
        #     # calulate probability for each attribute
        #     for att in self.testSet:
        #         if att != 'class':
        #             value = self.testSet[att][rowNumber]
        #             propsArray = self.mEstimate(att, value)
        #             allProbsArray.insert(len(allProbsArray), propsArray)
        #
        #     # multiplie same class and find final probability
        #     sameClassProbs = []
        #     # for val in range(len(allProbsArray[0])):
        #     #     multiplieProp = 1.0
        #     #     for probsArr in allProbsArray:
        #     #         multiplieProp *= probsArr[val]
        #     #     sameClassProbs.insert(len(sameClassProbs),
        #     #                           float(self.numberOfDifferentClassses[self.numberOfDifferentClassses.keys()[val]])
        #     #                           / float(self.numberOfRows) *
        #     #                           multiplieProp)
        #
        #     classValueIndex = 0
        #     for classValue in self.attributes['class']:
        #         multiplieProp = 1.0
        #         for probsArr in allProbsArray:
        #             multiplieProp *= probsArr[classValueIndex]
        #
        #         sameClassProbs.insert(len(sameClassProbs),
        #                             float(self.numberOfDifferentClassses[classValue])
        #                             / float(self.numberOfRows) *
        #                             multiplieProp)
        #
        #         classValueIndex = classValueIndex + 1
        #
        #     # find max
        #     maxValueIndex = sameClassProbs.index(max(sameClassProbs))
        #     # classification = self.attributes['class'][maxValueIndex]
        #     classification = self.attributes['class'][maxValueIndex]
        #     with open(self.builder.path + "\\output.txt", 'a') as output:
        #         output.write(str(rowNumber) + " " + classification + "\n")
        # print("Finished classifying all rows")
        # self.accuracy()

    def mEstimate(self, att, value):
        propsArr = []
        allAttval = self.trainingSet.groupby([att])[att].agg('count')  # needed to calc p
        m = 2.0
        p = 1.0 / len(allAttval)

        for classValue in self.attributes['class']:
            n = self.numberOfDifferentClassses[classValue]

            # get the count based on both - att ans "class" (nc)
            nc = self.trainingSet[(self.trainingSet[att] == value)
                                  & (self.trainingSet['class'] == classValue)][att].count()
            propOfAttAndClass = (nc + m * p) / (n + m)
            propsArr.append(propOfAttAndClass)

            # for i in range(classes):
            # n = self.numberOfDifferentClassses[i]
            #
            # #get the count based on both - att ans "class" (nc)
            # nc = self.trainingSet[(self.trainingSet[att] == value)
            #                       & (self.trainingSet['class'] == self.numberOfDifferentClassses.keys()[i])][att].count()
            # propOfAttAndClass = (nc + m*p)/(n + m)
            # propsArr.insert(len(propsArr), propOfAttAndClass)

        return propsArr

    def accuracy(self):
        with open(self.builder.path + "\\output.txt", 'r') as f:
            testOutput = f.readlines()
            matchLines = 0.0
            totlLines = 0.0
            for i in range(len(testOutput)):
                totlLines = totlLines + 1
                if self.testSet['class'].iloc[i] == testOutput[i].split()[1]:
                    matchLines = matchLines + 1.0
            accuracy = matchLines / totlLines
            print ("Accuracy is: " + str(accuracy))

