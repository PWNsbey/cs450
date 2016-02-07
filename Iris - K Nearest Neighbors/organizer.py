import random


# A class to hold all the attributes
class listedObject:
    data = []
    target = 0


class Organizer:
    listedObjectsList = []

    def __init__(self, rawData):
        # The master list
        listedObjectsList = [len(rawData.data)]

        # Loading up the master list...
        for x in range(len(rawData.data)):
            y = listedObject()
            y.data = rawData.data[x]
            y.target = rawData.target[x]
            self.listedObjectsList.append(y)
            # ... I get the feeling that I'm doing all this the hard way, but whatever.

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
        # clearing the random 150...
        #self.listedObjectsList.remove(150)