import random


class IONode:
    def __init__(self):
        self.isEndNode = False  # also, end nodes always are stuck right onto a neuron's output
        self.value = 0
        self.connections = []

        self.networkIndexRef = 0

    def update(self):
        if self.isEndNode:
            self.value = self.connections[0].outputValue

class NeuralConnection:
    def __init__(self):
        self.inputObject = None   # the input or neuron providing a value
        self.outputObject = None  # the output or neuron receiving a value

        self.weight = 0
        self.weightedValue = 0

        self.networkIndexRef = 0

    def update(self):
        self.computeWeightedValue()

    def computeWeightedValue(self):
        if isinstance(self.inputObject, IONode):
            self.weightedValue = self.inputObject.value * self.weight
        else:  # if not, it should be a Neuron. SHOULD.
            self.weightedValue = self.inputObject.outputValue * self.weight

class Neuron:
    def __init__(self):
        self.incomingConnections = []  # all connections linking to this neuron
        self.outgoingConnections = []  # all outgoing connections leaving this neuron
        self.biasNodeConnection = None

        self.threshold = 0
        self.outputValue = 0

        self.networkIndexRef = 0

    def update(self):
        # configure the bias
        if self.biasNodeConnection is None:
            self.biasNodeConnection = NeuralConnection()
            self.biasNodeConnection.inputObject = IONode()
            self.biasNodeConnection.weight = float(random.randint(-10, 10)/10)
            self.biasNodeConnection.inputObject.value = -1
            self.biasNodeConnection.networkIndexRef = -1
            self.biasNodeConnection.update()
            self.incomingConnections.append(self.biasNodeConnection)

        sum = 0
        for i in range(len(self.incomingConnections)):
            sum += self.incomingConnections[i].weightedValue

        if sum <= self.threshold:
            self.outputValue = 0
        else:
            self.outputValue = 1
