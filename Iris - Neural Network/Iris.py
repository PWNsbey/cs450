import BrainMatter as BM
from decimal import *
import LazyDevTools as lds


class Iris:
    def __init__(self):
        self.trainingExamples = []
        self.validationExamples = []

        # where len() is the number of layers, and [i] is the number of neurons
        self.nodeLayersArray = []

        # essentially a 2D array. holds each 'column' of the network.
        self.neuralNetwork = []

    def train(self, trainingExamples, nodeLayersArray):
        self.trainingExamples = trainingExamples
        self.nodeLayersArray = nodeLayersArray

        # split the examples into a training set and a validation set...
        fifthOfList = int(len(trainingExamples) / 5)
        self.validationExamples = trainingExamples.copy()
        for i in range(0, fifthOfList * 4):
            self.validationExamples.pop()
        for i in range(fifthOfList * 4, len(trainingExamples)):
            self.trainingExamples.pop()

        # initialize the neural network
        self.initializeNetwork(trainingExamples)
        self.printNetwork()
        self.connectNetLayers()

    def initializeNetwork(self, trainingExamples):
        print("Initializing network...")
        # input nodes
        inputNodes = []
        for i in range(len(trainingExamples[0].data)):
            inputNodes.append(BM.IONode)
        self.neuralNetwork.append(inputNodes)

        # now the body. alternating connections and neurons
        connectionNeuronArray = []  # temp array to append into the main one
        for i in range(len(self.nodeLayersArray)):  # for each layer...
            # connection layer
            for j in range(self.nodeLayersArray[i]):
                # one connection for each previous input * next layer
                previousInputLen = len(self.neuralNetwork[len(self.neuralNetwork) - 2])
                for k in range(1, (previousInputLen * self.nodeLayersArray[i])):
                    connectionNeuronArray.append(BM.NeuralConnection)
            self.neuralNetwork.append(connectionNeuronArray)

            #neuron layer
            for j in range(self.nodeLayersArray[i]):
                connectionNeuronArray.append(BM.Neuron)
            self.neuralNetwork.append(connectionNeuronArray)

        # finally, the output nodes
        outputNodes = []
        for i in range(len(self.neuralNetwork[len(self.neuralNetwork) - 1])):
            outputNodes.append(BM.IONode)
        self.neuralNetwork.append(outputNodes)

        print("Network initialized.")

    def connectNetLayers(self):
        for i in range(len(self.neuralNetwork)):
            if i == 0:  # if this in the input array...
                pass

            divConnectionNum = int(len(self.neuralNetwork[i + 1]) / len(self.neuralNetwork[i]))
            tempModNum = 0
            for j in range(len(self.neuralNetwork[i])):  # for each input node...
                for l in range(tempModNum, (tempModNum - 1) + divConnectionNum):
                    self.neuralNetwork[i][j].connections.append(self.neuralNetwork[i+1][l])
                    self.neuralNetwork[i+1][l].inputObject = self.neuralNetwork[i][j]
                tempModNum += divConnectionNum

            if i == len(self.neuralNetwork) - 2:  # if this is the final node array...
                for j in range(len(self.neuralNetwork[i])):
                    self.neuralNetwork[i][j].outgoingConnections.append(self.neuralNetwork[i+1][j])

            # standard procedure
            # neural connections
            if self.neuralNetwork[i][0] is BM.NeuralConnection:
                tempModNum = 0
                for j in range(tempModNum, (tempModNum - 1) + divConnectionNum):
                    self.neuralNetwork[i][j].outputObject = self.neuralNetwork[i+1][j]
                    self.neuralNetwork[i+1][j].incomingConnections.append(self.neuralNetwork[i][j])
                tempModNum += divConnectionNum
            else:  # neurons to connections
                divConnectionNum = int(len(self.neuralNetwork[i+1]) / len(self.neuralNetwork[i]))
                tempModNum = 0
                for j in range(len(self.neuralNetwork[i])):
                    for k in range(tempModNum, (tempModNum - 1) + divConnectionNum):
                        self.neuralNetwork[i][j].outgoingConnections.append(self.neuralNetwork[i][k])
                    tempModNum += divConnectionNum

    def printNetwork(self):
        netDisplayRow = []
        netDisplayCol = []

        # the "lowest-reaching" column in neuralNetwork
        maxColNumber = 0
        for i in range(len(self.neuralNetwork)):
            if len(self.neuralNetwork[i]) > maxColNumber:
                maxColNumber = len(self.neuralNetwork[i])

        for i in range(len(self.neuralNetwork)):
            for j in range(maxColNumber):
                if self.neuralNetwork[i][j]:
                    netDisplayRow.append(self.neuralNetwork[i][j])
                else:
                    netDisplayRow.append(None)
            netDisplayCol.append(netDisplayRow)

        # on to the display stuff
        for i in range(len(netDisplayRow)):
            printString = ""

            for j in range(len(netDisplayCol)):
                if netDisplayCol[i][j] is BM.IONode:
                    nodeAlias = netDisplayCol[i][j]

                    if nodeAlias.isEndNode:
                        connectionRef = netDisplayCol[i-1].index(nodeAlias.connections[0])
                        printString += str(connectionRef) + "<" + str(nodeAlias.value)
                    else:
                        connectionRef = netDisplayCol[i-1].index(nodeAlias.connections[0])
                        printString += str(nodeAlias.value) + ">" + str(connectionRef)
                    printString += " "
                elif netDisplayCol[i][j] is BM.NeuralConnection:
                    connectionAlias = netDisplayCol[i][j]
                    incoming = netDisplayCol[i-1].index(connectionAlias.inputObject)
                    outgoing = netDisplayCol[i+1].index(connectionAlias.outputObject)

                    valuesString = "--w" + str(connectionAlias.weight) + "v" + str(connectionAlias.weightedValue)
                    print("-" + str(incoming) + valuesString + str(outgoing) + "-")
                else:  # is neurons
                    pass

            print(printString)
