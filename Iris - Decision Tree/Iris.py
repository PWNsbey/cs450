from Node import Node
from DataWizard import Wizard
import numpy as np
import LazyDevTools as lds

class Iris:
    def __init__(self, discreteRefList, wizard):
        # need to have a handy dandy wizard on hand
        self.wizard = wizard

        # set the ref list
        self.discreteRefList = discreteRefList

        self.startingNode = None  # not set until train()

        self.accuracy = 0

    def train(self, examplesList):
        usedAttributes = []
        self.startingNode = Node(examplesList, self.discreteRefList, usedAttributes)

        self.startingNode.activate_node()

    def categorize(self, unknownExamples):
        classifiedTargetsList = []

        for i in range(len(unknownExamples)):
            classifiedTargetsList.append(self.recurseClassify(unknownExamples[i], self.startingNode))

        numberCorrect = 0
        for i in range(len(unknownExamples)):
            if classifiedTargetsList[i] == unknownExamples[i].target:
                numberCorrect += 1
        self.accuracy = numberCorrect/(len(unknownExamples))

    def recurseClassify(self, example, node):
        if node.isLeafNode:
            return self.wizard.find_majority_type(node.examplesList)
        else:
            attribute = node.splittingOnAttribute
            for i in range(len(node.childNodes)):
                if example.data[attribute] == node.childNodes[i].examplesList[0].data[attribute]:
                    return self.recurseClassify(example, node.childNodes[i])

    def printTree(self, node=None, i=0):
        if node is None:
            node = self.startingNode

        examplesString = ""
        dictionaryString = ""
        attributesString = ""
        tabsString = ""

        nodeString = ""
        if node.isLeafNode:
            nodeString += "*LEAF*"
        nodeString += "Node-" + str(node.entropyValue) + "(" + str(len(node.examplesList)) + "):"

        for j in range(len(node.examplesList)):
            examplesString += str(node.examplesList[j].target) + " "
        for j in range(len(node.dictionary)):
            dictionaryString += str(j) + ":" + str(node.dictionary[j]) + " "
        for j in range(len(node.usedAttributes)):
            attributesString += str(node.usedAttributes[j]) + " "
        for j in range(i):
            tabsString += "\t"

        print(tabsString, nodeString, examplesString)
        print(tabsString, "Dictionary-" + dictionaryString)
        print(tabsString, "UsedAttributes(" + str(len(node.usedAttributes)) + ")-", attributesString)
        print(tabsString, "~~~~~~~~~~~~~~~~~~~~~")

        for j in range(len(node.childNodes)):
            self.printTree(node.childNodes[j], i + 1)