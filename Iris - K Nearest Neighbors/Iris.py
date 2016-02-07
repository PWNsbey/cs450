import numpy as np
from scipy import stats

# The classifier itself.
class Iris:
    totalObjects = 0
    correctResults = 0

    categorizedObjects = []

    # trains Iris by adding objects to the categorizedObjects array
    def train(self, trainingSet):
        for i in range(len(trainingSet)):
            self.categorizedObjects.append(trainingSet[i])

    # attempts to categorize objects Iris has never seen before
    def predict(self, testingSet, kNumber):
        self.totalObjects = len(testingSet)
        returnList = []

        for i in range(len(testingSet)):  # for each incoming object to predict...
            # ... find its kNumber-nearest peers...
            peersList = self.find_k_nearest_neighbors(self.find_target_dist(testingSet[i].data), kNumber)
            # ... then choose the majority class type and add it to the list
            returnList.append(self.find_majority(peersList))

        # print the returnList
        for i in range(len(returnList)):
            print("returnList:", returnList[i])
        print("==============================================")

        self.check_correctness(returnList, testingSet)  # quick internal check. Display results by calling
        return returnList;                              # percent_correct() from elsewhere.

    # Returns an array of kNumber near neighbors
    def find_k_nearest_neighbors(self, targetDists, kNumber): # where targetDists is the array of dists from neighbors
        nearestNeighborsList = []

        for i in range(kNumber): # find kNumber of nearest neighbors...
            smallestDist = targetDists[0]           # the smallest dist in this iteration
            smallestDistIndex = 0                   # the corresponding reference in categorizedObjects

            for j in range(len(targetDists)): # ...in the list of dists
                if targetDists[j] < smallestDist:
                    smallestDist = targetDists[j]
                    smallestDistIndex = j
            nearestNeighborsList.append(self.categorizedObjects[smallestDistIndex])
            targetDists[smallestDistIndex] += 1000  # make sure this one isn't picked again

        return nearestNeighborsList

    # returns a list of the distances of each dimension between the target and examples
    def find_target_dist(self, target):
        dist_from_peers = []

        # # Normalize all the data
        # target = stats.zscore(target)

        # for i in range(len(self.categorizedObjects)):
        #     self.categorizedObjects[i].data = stats.zscore(self.categorizedObjects[i].data)

        # calculate the distance
        for i in range(len(self.categorizedObjects)):
            subtractedTotal = 0
            for j in range(len(target)):
                subtractedTotal += ((target[j])**2) - ((self.categorizedObjects[i].data[j])**2)
            dist_from_peers.append(abs(subtractedTotal)) # absolute value here to make things easier later

        return dist_from_peers;

    def find_majority(self, nearestNeighborsList):
        majorityNeighborType = nearestNeighborsList[0].target # The most common class of object
        allNeighborTypesArray = []

        # indexing all the object classes
        for i in range(len(nearestNeighborsList)):
            allNeighborTypesArray.append(nearestNeighborsList[i].target)

        # count 'em up
        largestTotal = 0
        for i in range (len(allNeighborTypesArray)):
            if allNeighborTypesArray.count(allNeighborTypesArray[i]) > largestTotal:
                largestTotal = allNeighborTypesArray.count(allNeighborTypesArray[i])
                majorityNeighborType = allNeighborTypesArray[i]

        return majorityNeighborType

    def check_correctness(self, results, testingSet):
        for i in range(len(results)):
            if results[i] == testingSet[i].target:
                self.correctResults += 1

    def percent_correct(self):
        return self.correctResults / self.totalObjects;