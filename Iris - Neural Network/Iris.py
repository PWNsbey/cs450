import BrainMatter as BM
import random


class Iris:
    def __init__(self):
        self.trainingExamples = []
        self.validationExamples = []

        # where len() is the number of layers, and [i] is the number of neurons
        self.nodeLayersArray = []

        # essentially a 2D array. holds each 'column' of the network.
        self.neuralNetwork = []
        # this holds each iteration of the network between training batches.
        self.networkArchive = []
        self.accuracyArchive = []
        self.validAccuracyArchive = []

        # how fast weights are modified
        self.learningRate = .1

        # the accuracy of this version of Iris! Given in percentage (float between 0 and 1)
        self.accuracy = 0
        self.validAccuracy = 0  # the accuracy of the validation set

    def train(self, trainingExamples, nodeLayersArray):
        self.trainingExamples = trainingExamples
        self.nodeLayersArray = nodeLayersArray

        # clear the network
        for i in range(len(self.neuralNetwork)):
            self.neuralNetwork.pop()
        # reset the accuracy
        self.accuracy = 0

        # split the examples into a training set and a validation set...
        fifthOfList = int(len(self.trainingExamples) / 5)
        self.validationExamples = self.trainingExamples.copy()
        for i in range(0, fifthOfList * 4):
            self.validationExamples.pop()
        for i in range(fifthOfList * 4, len(self.trainingExamples)):
            self.trainingExamples.pop()
        random.shuffle(self.trainingExamples)

        # initialize the neural network
        self.initializeNetwork(self.trainingExamples)
        self.connectNetLayers()
        self.updateNetwork(0)

        # begin training!
        for i in range(len(self.trainingExamples)):
            self.updateNetwork(i)  # standard - just moves values through the network
            self.exactDiscipline(i)  # actually modifies the weights. This is where the learning happens.

        self.test(self.validationExamples)
        self.networkArchive.append(self.neuralNetwork)
        self.accuracyArchive.append(self.accuracy)

    def test(self, testingExamples):
        numCorrect = 0  # what it says on the tin
        for i in range(len(testingExamples)):
            self.updateNetwork(i)  # just the standard stuff - no learning

            # lets check for accuracy now.
            outputNodesAlias = self.neuralNetwork[len(self.neuralNetwork) - 1]
            target = testingExamples[i].target

            badNeurons = self.findBadNeurons(i, outputNodesAlias, target)
            if badNeurons.count(True) == 0:
                numCorrect += 1

        self.accuracy = round(numCorrect/len(testingExamples), 2)

    def initializeNetwork(self, trainingExamples):
        print("Initializing network...")
        # input nodes
        inputNodes = []
        for i in range(len(trainingExamples[0].data)):
            inputNode = BM.IONode()
            inputNodes.append(inputNode)
        self.neuralNetwork.append(inputNodes)
        print("Input nodes initialized with", len(inputNodes), "nodes.")

        # now the body. alternating connections and neurons
        connectionNeuronArray = []  # temp array to append into the main one
        for i in range(len(self.nodeLayersArray)):  # for each layer...
            # connection layer
            for j in range(self.nodeLayersArray[i]):
                # one connection for each previous input * next layer
                previousInputLen = len(self.neuralNetwork[len(self.neuralNetwork) - 2])
                for k in range(previousInputLen):
                    connection = BM.NeuralConnection()
                    connection.weight = float(random.randint(-10, 10)/10)
                    connectionNeuronArray.append(connection)
            self.neuralNetwork.append(connectionNeuronArray)
            print("Connection layer initialized with", len(connectionNeuronArray), "connections.")

            #neuron layer
            connectionNeuronArray = []
            for j in range(self.nodeLayersArray[i]):
                neuron = BM.Neuron()
                connectionNeuronArray.append(neuron)
            self.neuralNetwork.append(connectionNeuronArray)
            print("Neuron layer initialized with    ", len(connectionNeuronArray), "neurons.")

        # finally, the output nodes
        outputNodes = []
        for i in range(len(self.neuralNetwork[len(self.neuralNetwork) - 1])):
            outputNode = BM.IONode()
            outputNodes.append(outputNode)
            # make sure the node knows this is the end
            outputNodes[i].isEndNode = True
        self.neuralNetwork.append(outputNodes)
        print("Output nodes initialized with", len(outputNodes), "endNodes.")

        # sets the index numbers for each network element so I don't have to do any more index() nonsense
        self.setRefNumbers()

        print("===Network fully initialized!===")

    # simply loops through the network and gives each element its own index reference number.
    def setRefNumbers(self):
        for i in range(len(self.neuralNetwork)):
            for j in range(len(self.neuralNetwork[i])):
                self.neuralNetwork[i][j].networkIndexRef = j
                print("refNumber set to:", self.neuralNetwork[i][j].networkIndexRef)

    # connects element i's output to the next element's input. Connects next input back to i's output.
    def connectNetLayers(self):
        for i in range(len(self.neuralNetwork) - 1):
            # inputNode - neuralConnection
            if i == 0:
                connectionIndex = 0  # keeps track of which connection can next be claimed by an inputNode
                for j in range(len(self.neuralNetwork[i])):  # for each input node
                    print("connecting inputNode to connection...")
                    for k in range(len(self.neuralNetwork[i+2])):  # one connection per neuron
                        # connect i to i+1
                        self.neuralNetwork[i][j].connections.append(self.neuralNetwork[i+1][connectionIndex])
                        # connect i+1 to i
                        self.neuralNetwork[i+1][connectionIndex].inputObject = self.neuralNetwork[i][j]
                        # this connection is now claimed. Increment the index counter
                        connectionIndex += 1

            # neuralConnection - Neuron
            elif isinstance(self.neuralNetwork[i][0], BM.NeuralConnection):
                # the number of connections that come from each input. They lie in chunks together in the list
                inputChunkSize = len(self.neuralNetwork[i+1])
                # the relative number of this connection in the chunk
                # also corresponds to which neuron gets this (j) connection
                currentChunkMember = 0
                for j in range(len(self.neuralNetwork[i])):  # for each connection
                    print("connecting connection to neuron...")
                    # set the relative number to 0 if we're in the next chunk already
                    if currentChunkMember >= inputChunkSize:
                        currentChunkMember = 0
                    # connect i to i+1
                    self.neuralNetwork[i][j].outputObject = self.neuralNetwork[i+1][currentChunkMember]
                    # connect i+1 to i
                    self.neuralNetwork[i+1][currentChunkMember].incomingConnections.append(self.neuralNetwork[i][j])
                    # update the inter-chunk reference number
                    currentChunkMember += 1

            # neuron - neuralConnection
            elif isinstance(self.neuralNetwork[i][0], BM.Neuron) and isinstance(self.neuralNetwork[i+1][0], BM.NeuralConnection):
                connectionIndex = 0  # keeps track of which connection can next be claimed by a neuron
                for j in range(len(self.neuralNetwork[i])):  # for each neuron
                    print("connecting neuron to connection...")
                    for k in range(len(self.neuralNetwork[i+2])):  # one connection per next-layer neuron
                        # connect i to i+1
                        self.neuralNetwork[i][j].outgoingConnections.append(self.neuralNetwork[i+1][connectionIndex])
                        # connect i+1 to i
                        self.neuralNetwork[i+1][connectionIndex].inputObject = self.neuralNetwork[i][j]
                        # this connection is now claimed. Increment the index counter
                        connectionIndex += 1

            # neuron - endNode
            # this one is a one-to-one relationship, so it's pretty straightforward
            elif i == len(self.neuralNetwork) - 2:
                for j in range(len(self.neuralNetwork[i])):  # for each neuron
                    print("connecting neuron to endNode")
                    # connect i to i+1
                    self.neuralNetwork[i][j].outgoingConnections.append(self.neuralNetwork[i+1][j])
                    # connect i+1 to i
                    self.neuralNetwork[i+1][j].connections.append(self.neuralNetwork[i][j])

        print("===All layers connected!===")

    # moves all values through the network
    def updateNetwork(self, exampleNumber):
        for i in range(len(self.neuralNetwork)):
            for j in range(len(self.neuralNetwork[i])):
                # The first IONodes should get raw values, not be updated
                if i == 0:
                    self.neuralNetwork[i][j].value = self.trainingExamples[exampleNumber].data[j]
                # everything else just runs their update functions
                else:
                    self.neuralNetwork[i][j].update()

    # corrects weight values. This is where the learning happens.
    def exactDiscipline(self, exampleNumber):
        outputNodesAlias = self.neuralNetwork[len(self.neuralNetwork) - 1]
        target = self.trainingExamples[exampleNumber].target

        targetArray = []
        # populate the target array
        for i in range(self.nodeLayersArray[len(self.nodeLayersArray) - 1]):
            targetArray.append(0)
        # now convert it to binary format
        targetArray[target] = 1

        badNeurons = self.findBadNeurons(exampleNumber, outputNodesAlias, target)

        for i in range(len(badNeurons)):
            if badNeurons[i] == False:  # Good on you, neuron. Move along.
                pass
            else:  # ITS TIME FOR YOUR RE-EDUCATION, SINFUL NEURON
                neuronAlias = outputNodesAlias[badNeurons[i]].connections[0]
                output = neuronAlias.outputValue
                # technically, we work with Connections here, but I still blame the neuron.
                for j in range(len(neuronAlias.incomingConnections)):
                    connection = neuronAlias.incomingConnections[j]
                    outputError = output * (1 - output) * (output - targetArray[i])
                    connection.weight = connection.weight - (self.learningRate) * outputError * connection.weightedValue
                    print("weight set to", connection.weight)

    # returns a list of all the neurons that don't line up with the targets
    def findBadNeurons(self, exampleNumber, outputNodesAlias, target):
        # First, a bunch of variables...
        badNeurons = []
        targetArray = []
        resultArray = []
        # populate the target array
        for i in range(self.nodeLayersArray[len(self.nodeLayersArray) - 1]):
            targetArray.append(0)
        # now convert it to binary format
        targetArray[target] = 1
        # populate the result array. This is the actual output of the network.
        for i in range(len(outputNodesAlias)):
            resultArray.append(outputNodesAlias[i].value)

        # Right, that's enough with the variables. Now on to DISCIPLINE.
        # First, a comparison.
        for i in range(len(targetArray)):
            if targetArray[i] != resultArray[i]:
                badNeurons.append(True)  # YOU HAVE FAILED US
            else:
                badNeurons.append(False)

        return badNeurons

    # prints the network in its own html file. So fancy.
    def printNetwork(self, neuralNetwork):
        # i corresponds to <tr>s.
        tableContentString = "<table><tr>"
        for i in range(len(neuralNetwork)):
            # j corresponds to <td>s.
            tableContentString += "<td>"
            for j in range(len(neuralNetwork[i])):
                tableContentString += self.stringify(neuralNetwork, i, j) + "<br>"
            # finisher strings below. Don't panic.
            tableContentString += "</td>"
        tableContentString += "<br><br>This network's accuracy: " + str(self.accuracy) + "</tr></table>"

        # this is what actually goes in the file
        headString = "<head><link rel=\"stylesheet\" type=\"text/css\" href=\"stylesheet.css\"/></head>"
        htmlString = "<!DOCTYPE html><html>" + headString + "<body>" + tableContentString + "</body></html>"

        file = open("networkVisual.html", "w")
        file.write(htmlString)
        file.close()

    # makes a fancy-looking string object for each type of object in the network
    def stringify(self, neuralNetwork, i, j):
        fancyString = ""
        objectAlias = neuralNetwork[i][j]

        # handle BOTH input AND output nodes
        if isinstance(objectAlias, BM.IONode):
            # inputNodes
            if objectAlias.isEndNode == False:
                # value and symbol
                fancyString = "<b>" + str(objectAlias.value) + "></b>"
                # add all connections
                for i in range(len(objectAlias.connections)):
                    fancyString += str(objectAlias.connections[i].networkIndexRef)
                    # if it isn't the last connection, add a comma and a space
                    if i < len(objectAlias.connections) - 1:
                        fancyString += ", "
            # outputNodes
            else:
                # add all connections
                for i in range(len(objectAlias.connections)):
                    fancyString += str(objectAlias.connections[i].networkIndexRef)
                    # if it isn't the last connection, add a comma
                    if i != len(objectAlias.connections) - 1:
                        fancyString += ","
                # symbol and value
                fancyString += "<b><" + str(objectAlias.value) + "</b>"

        # handle connections
        elif isinstance(objectAlias, BM.NeuralConnection):
            fancyString = str(objectAlias.inputObject.networkIndexRef)
            # makes sure that everything lines up pretty because the negative signs are triggering my OCD
            if objectAlias.weight >= 0:
                fancyString += "<b>---w: " + str(round(objectAlias.weight, 1))
            else:
                fancyString += "<b>---w:" + str(round(objectAlias.weight, 1))
            # same here
            if objectAlias.weightedValue >= 0:
                fancyString += " v: " + str(round(objectAlias.weightedValue, 1)) + "---</b>"
            else:
                fancyString += " v:" + str(round(objectAlias.weightedValue, 1)) + "---</b>"
            fancyString += str(objectAlias.outputObject.networkIndexRef)

        # handle neurons
        elif isinstance(objectAlias, BM.Neuron):
            # add all incoming connections
            # if there's no number bigger than 9 here, add a space because OCD
            hasGreaterThanTen = False
            for i in range(len(objectAlias.incomingConnections)):
                # ocd check
                if objectAlias.incomingConnections[i].networkIndexRef > 9:
                    hasGreaterThanTen = True
                # now the string append
                fancyString += str(objectAlias.incomingConnections[i].networkIndexRef)
                # if it isn't the last connection, add a comma
                if i < len(objectAlias.incomingConnections) - 1:
                    fancyString += ","
                # we want to add that OCD space before the -1 that indicates the bias node
                if i == len(objectAlias.incomingConnections) - 2:
                    if hasGreaterThanTen == False:
                        fancyString += " "

            # add inner values
            fancyString += "<b>[t:" + str(objectAlias.threshold) + "v:" + str(objectAlias.outputValue) + "]</b>"
            # add all outgoing connections
            for i in range(len(objectAlias.outgoingConnections)):
                fancyString += str(objectAlias.outgoingConnections[i].networkIndexRef)
                # if it isn't the last connection, add a comma
                if i < len(objectAlias.outgoingConnections) - 1:
                    fancyString += ","

        return fancyString
