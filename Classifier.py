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
        propsArr = []
        classes = len(self.numberOfDifferentClassses)
        allAttval = self.trainingSet.groupby([att])[att].agg('count')  #needed to calc p
        m = 2.0
        p = 1.0/len(allAttval)

        for i in range(classes) :
            n = self.numberOfDifferentClassses[i]
            #get the count based on both - att ans "class" (nc)
            nc = self.trainingSet[(self.trainingSet[att] == 0)
                                  & (self.trainingSet['class'] == self.numberOfDifferentClassses.keys()[i])][att].count()
            propOfAttAndClass = (nc + m*p)/(n + m)
            propsArr.insert(len(propsArr), propOfAttAndClass)

        return propsArr

    def accuracy(self):
        with open(self.builder.path+"\\output.txt", 'r') as f:
            testOutput = f.readlines()
            matchLines = 0.0
            totlLines = 0.0
            for i in range(len(testOutput)):
                totlLines = totlLines + 1
                if(self.testSet['class'].iloc[i] == testOutput[i].split()[1]):
                    matchLines = matchLines+1.0
            accuracy = matchLines/totlLines
            print ("Accuracy is: "+accuracy)







