import numpy as np
import LazyDevTools as lds


class Node:
    discreteRefList = []  # where i is the attribute reference number, and [i] returns the number of discrete bins

    dictionary = []  # dictionary[i] where i is the target and [i] returns the total number of this type

    usedAttributes = []  # all used example attributes used by this node's parents
    childNodes = []

    entropyValue = 0

    def __init__(self, examplesList, discreteRefList, usedAttributes, splittingOnAttribute=0):
        # populate the node
        self.examplesList = examplesList

        # set the already-used attributes
        self.usedAttributes = list(usedAttributes)

        # set the attribute this node was split on
        self.splittingOnAttribute = splittingOnAttribute

        # is this a leaf node?
        self.isLeafNode = False

        # set the bin numbers for the discretized attributes
        self.discreteRefList = discreteRefList

        # clear the dictionary
        newDictionary = []
        for i in range(len(self.discreteRefList) - 1):  # -1 because len() is not 0-based. Lists are.
            newDictionary.append(0)
        self.dictionary = newDictionary

        # populate the dictionary
        for i in range(len(self.examplesList)):
            self.dictionary[self.examplesList[i].target] += 1

        # now that we have the node and dictionary populated, calculate the entropy
        self.calc_entropy()

    # signals this node to begin reproducing
    def activate_node(self):
        # set the isLeafNode variable
        self.check_is_leaf_node()

        # if this isn't a leaf node, reproduce
        if self.isLeafNode != True:
            self.childNodes = self.create_optimal_children()

            # switch 'em on recursively
            for i in range(len(self.childNodes)):
                self.childNodes[i].activate_node()

    # sets the entropy value for this node
    def calc_entropy(self):
        for i in range(len(self.dictionary)):  # for each target type:
            if self.dictionary[i] != 0:
                p = self.dictionary[i]/len(self.examplesList)  # probability
                self.entropyValue += -p * np.log2(p)    # entropy

    # what it says on the tin.
    def check_is_leaf_node(self):
        if self.entropyValue == 0:  # if all examples are the same target class...
            self.isLeafNode = True

        if len(self.usedAttributes) == len(self.discreteRefList):  # if all attributes are used up...
            self.isLeafNode = True

    # not a heartless display of reproduction. picks an attribute with the least entropic results, and returns that gen
    def create_optimal_children(self):
        generationOptions = []

        # create a list of all possible generations
        for i in range(len(self.discreteRefList)):
            if self.usedAttributes.count(i) == 0:
                generationOptions.append(self.create_node_generation(i))

        optimalGeneration = generationOptions[0]
        usedAttribute = 0

        # find the one with the least entropy
        for i in range(len(generationOptions)):
            generationEntropy = self.find_generation_entropy(generationOptions[i])
            # if the total average entropy of this generation is better than the previous best, it is the new best
            if generationEntropy > self.find_generation_entropy(optimalGeneration):
                optimalGeneration = generationOptions[i]
                usedAttribute = i

        self.usedAttributes.append(usedAttribute)
        self.splittingOnAttribute = usedAttribute
        return optimalGeneration

    # returns a set of node children based on the given attribute
    def create_node_generation(self, attributeRef):
        # where i corresponds to the attribute value, and [i] returns an array of the examples
        sortedChildrenExamples = []
        nodeGeneration = []

        for i in range(len(self.examplesList)):
            # if the example's attribute bin number doesn't exist yet...
            if sortedChildrenExamples.count(self.examplesList[i].data[attributeRef]) == 0:
                # add all number slots in between
                for j in range((self.examplesList[i].data[attributeRef] + 1) - len(sortedChildrenExamples)):
                    sortedChildrenExamples.append([])

            # now sort the example
            sortedChildrenExamples[self.examplesList[i].data[attributeRef]].append(self.examplesList[i])

        usedAttributes = list(self.usedAttributes)
        usedAttributes.append(attributeRef)

        for i in range(len(sortedChildrenExamples)):
            if len(sortedChildrenExamples[i]) != 0:
                nodeGeneration.append(Node(sortedChildrenExamples[i], self.discreteRefList, usedAttributes))

        return nodeGeneration

    # returns the average entropy of a given generation
    def find_generation_entropy(self, nodeGeneration):
        totalEntropy = 0
        for i in range(len(nodeGeneration)):
            totalEntropy += nodeGeneration[i].entropyValue

        totalEntropy /= len(nodeGeneration)
        return totalEntropy
