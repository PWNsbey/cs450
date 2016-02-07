import random
import numpy as np
import LazyDevTools as lds


# A class to hold all the attributes
class listedObject:
    data = []
    target = 0


class Wizard:
    listedObjectsList = []

    #
    def __init__(self, rawData, discreteRefList = []):
        # Loading up the master list...
        for x in range(len(rawData.data)):
            y = listedObject()
            y.data = rawData.data[x]
            y.target = rawData.target[x]
            self.listedObjectsList.append(y)
            # ... I get the feeling that I'm doing all this the hard way, but whatever.

        # if the user passed in a ref list, discretize the data
        if len(discreteRefList) > 0:
            self.discretizeData(discreteRefList)

    def find_majority_type(self, examplesList):
        allTargetTypes = []
        for i in range(len(examplesList)):
            allTargetTypes.append(examplesList[i].target)

        targetDictionary = []
        for i in range(np.amax(allTargetTypes) + 1):
            targetDictionary.append(0)

        for i in range(len(allTargetTypes)):
            targetDictionary[allTargetTypes[i]] += 1

        majorityType = 0
        for i in range(len(targetDictionary)):
            if targetDictionary[i] > targetDictionary[majorityType]:
                majorityType = i

        return majorityType

    # Returns an array of two elements where [0] is the training set and [1] is the testing set
    def organize_data(self):
        self.randomize_list()

        # dividing up listedObjectsList for splitting into train/test sets
        tenthOfListLen = len(self.listedObjectsList) / 10

        # build the training set
        trainingSet = self.listedObjectsList.copy()
        for i in range(int(tenthOfListLen * 7), len(self.listedObjectsList)):
            trainingSet.pop()

        # build the testing set
        testingSet = self.listedObjectsList.copy()
        for i in range(0, len(self.listedObjectsList) - int(tenthOfListLen * 3)):
            testingSet.pop()

        trainTestSets = [trainingSet, testingSet]
        return trainTestSets;

    def randomize_list(self):
        # randomizing...
        random.shuffle(self.listedObjectsList)

    # discretizes the data in listedObjectsList[]
    # if discreteRefList[i] == 0, there will be no discretization for this attribute
    def discretizeData(self, discreteRefList):
        # where i = the attribute ref number and [i] returns an array of ALL attribute values in this category
        allAttributes = []

        # constructing the allAttributes array
        # for each example...
        for i in range(len(discreteRefList)):
            valueArray = []
            # and for each of the attribute types in it...
            for j in range(len(self.listedObjectsList)):
                valueArray.append(self.listedObjectsList[j].data[i])  # otherwise just add the attribute
            allAttributes.append(valueArray)

        # now the mathy bit
        allBinsArray = []  # where i = the attribute number and [i] returns the array of bins associated with it
        binArray = []
        for i in range(len(allAttributes)):
            if discreteRefList[i] != 0:  # only discretize if the refList says so
                # finding bin size
                maxVal = np.amax(allAttributes[i])
                minVal = np.amin(allAttributes[i])
                binSize = (maxVal - minVal) / discreteRefList[i]

                # build the bins
                for j in range(discreteRefList[i]):
                    roundedNumber = round(((binSize * j) + minVal), 2)
                    binArray.append(roundedNumber)
            allBinsArray.append(binArray)
            binArray = []  # clear the array

        for i in range(len(self.listedObjectsList)):  # for each example...
            for j in range(len(self.listedObjectsList[i].data)):  # and for each attribute...
                currAttribute = self.listedObjectsList[i].data[j]

                # begin the sorting! But only do it if refList says that's cool.
                if discreteRefList[j] != 0:
                    for k in range(len(allBinsArray[j])):  # for each attribute bin...
                        if currAttribute >= round(allBinsArray[j][k], 2):
                            self.listedObjectsList[i].data[j] = k
            self.listedObjectsList[i].data = list(map(int, self.listedObjectsList[i].data))
